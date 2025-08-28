/**
 * @file hal_cpu_arm_cortex.c
 * @brief HAL implementation for ARM Cortex-A CPU lane
 * @version 22.0
 * @date 2025-08-28
 * 
 * Implementation of HAL interface for ARM Cortex-A CPU compute lane
 * Provides deterministic execution with WCET monitoring for DAL-A compliance
 */

#include "hal_interface.h"
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/time.h>

/* CPU Lane Implementation */

/* Private data structures */
typedef struct {
    hal_job_t job;
    hal_result_t result;
    bool active;
    pthread_t thread;
    struct timespec start_time;
} cpu_job_slot_t;

typedef struct {
    bool initialized;
    bool online;
    hal_config_t config;
    cpu_job_slot_t job_slots[32];  // Max 32 concurrent jobs
    pthread_mutex_t mutex;
    uint32_t next_job_id;
    
    // Statistics
    uint64_t jobs_submitted;
    uint64_t jobs_completed;
    uint64_t jobs_failed;
    uint64_t total_execution_time_us;
    
    // Performance monitoring
    uint32_t cpu_usage_percent;
    uint32_t temperature_celsius;
    
} cpu_lane_context_t;

static cpu_lane_context_t g_cpu_context = {0};

/* Forward declarations */
static void* cpu_job_worker(void* arg);
static uint32_t cpu_calculate_checksum(const void* data, size_t size);
static uint64_t cpu_get_time_us(void);
static hal_error_t cpu_execute_function(const hal_job_t* job, hal_result_t* result);

/* HAL CPU Implementation */

hal_error_t hal_cpu_init(const hal_config_t* config) {
    if (!config || config->lane != HAL_LANE_CPU) {
        return HAL_ERROR_INVALID_PARAM;
    }
    
    pthread_mutex_lock(&g_cpu_context.mutex);
    
    if (g_cpu_context.initialized) {
        pthread_mutex_unlock(&g_cpu_context.mutex);
        return HAL_SUCCESS;
    }
    
    // Initialize context
    memset(&g_cpu_context, 0, sizeof(g_cpu_context));
    g_cpu_context.config = *config;
    g_cpu_context.online = true;
    g_cpu_context.next_job_id = 1;
    g_cpu_context.temperature_celsius = 45;  // Simulated
    
    pthread_mutex_init(&g_cpu_context.mutex, NULL);
    
    g_cpu_context.initialized = true;
    
    pthread_mutex_unlock(&g_cpu_context.mutex);
    
    return HAL_SUCCESS;
}

hal_error_t hal_cpu_shutdown(void) {
    pthread_mutex_lock(&g_cpu_context.mutex);
    
    if (!g_cpu_context.initialized) {
        pthread_mutex_unlock(&g_cpu_context.mutex);
        return HAL_SUCCESS;
    }
    
    // Cancel all running jobs
    for (int i = 0; i < 32; i++) {
        if (g_cpu_context.job_slots[i].active) {
            pthread_cancel(g_cpu_context.job_slots[i].thread);
            pthread_join(g_cpu_context.job_slots[i].thread, NULL);
            g_cpu_context.job_slots[i].active = false;
        }
    }
    
    g_cpu_context.online = false;
    g_cpu_context.initialized = false;
    
    pthread_mutex_unlock(&g_cpu_context.mutex);
    pthread_mutex_destroy(&g_cpu_context.mutex);
    
    return HAL_SUCCESS;
}

hal_error_t hal_cpu_submit_job(const hal_job_t* job) {
    if (!job) {
        return HAL_ERROR_INVALID_PARAM;
    }
    
    pthread_mutex_lock(&g_cpu_context.mutex);
    
    if (!g_cpu_context.initialized || !g_cpu_context.online) {
        pthread_mutex_unlock(&g_cpu_context.mutex);
        return HAL_ERROR_LANE_OFFLINE;
    }
    
    // Find free job slot
    int slot_index = -1;
    for (int i = 0; i < 32; i++) {
        if (!g_cpu_context.job_slots[i].active) {
            slot_index = i;
            break;
        }
    }
    
    if (slot_index == -1) {
        pthread_mutex_unlock(&g_cpu_context.mutex);
        return HAL_ERROR_BUSY;
    }
    
    cpu_job_slot_t* slot = &g_cpu_context.job_slots[slot_index];
    
    // Copy job and assign ID
    slot->job = *job;
    slot->job.job_id = g_cpu_context.next_job_id++;
    slot->active = true;
    
    // Initialize result
    memset(&slot->result, 0, sizeof(slot->result));
    slot->result.job_id = slot->job.job_id;
    slot->result.lane = HAL_LANE_CPU;
    slot->result.status = HAL_STATUS_PENDING;
    
    // Create worker thread
    if (pthread_create(&slot->thread, NULL, cpu_job_worker, slot) != 0) {
        slot->active = false;
        pthread_mutex_unlock(&g_cpu_context.mutex);
        return HAL_ERROR_HARDWARE;
    }
    
    g_cpu_context.jobs_submitted++;
    
    pthread_mutex_unlock(&g_cpu_context.mutex);
    
    return HAL_SUCCESS;
}

hal_error_t hal_cpu_wait_job(uint32_t job_id, hal_result_t* result, uint32_t timeout_us) {
    if (!result) {
        return HAL_ERROR_INVALID_PARAM;
    }
    
    struct timespec timeout_abs;
    clock_gettime(CLOCK_REALTIME, &timeout_abs);
    timeout_abs.tv_sec += timeout_us / 1000000;
    timeout_abs.tv_nsec += (timeout_us % 1000000) * 1000;
    if (timeout_abs.tv_nsec >= 1000000000) {
        timeout_abs.tv_sec++;
        timeout_abs.tv_nsec -= 1000000000;
    }
    
    cpu_job_slot_t* slot = NULL;
    
    // Find job slot
    pthread_mutex_lock(&g_cpu_context.mutex);
    for (int i = 0; i < 32; i++) {
        if (g_cpu_context.job_slots[i].active && 
            g_cpu_context.job_slots[i].job.job_id == job_id) {
            slot = &g_cpu_context.job_slots[i];
            break;
        }
    }
    pthread_mutex_unlock(&g_cpu_context.mutex);
    
    if (!slot) {
        return HAL_ERROR_INVALID_PARAM;
    }
    
    // Wait for completion
    void* thread_result;
    int join_result = pthread_timedjoin_np(slot->thread, &thread_result, &timeout_abs);
    
    if (join_result != 0) {
        return HAL_ERROR_TIMEOUT;
    }
    
    // Copy result
    *result = slot->result;
    
    // Mark slot as free
    pthread_mutex_lock(&g_cpu_context.mutex);
    slot->active = false;
    pthread_mutex_unlock(&g_cpu_context.mutex);
    
    return HAL_SUCCESS;
}

hal_error_t hal_cpu_poll_job(uint32_t job_id, hal_result_t* result) {
    if (!result) {
        return HAL_ERROR_INVALID_PARAM;
    }
    
    pthread_mutex_lock(&g_cpu_context.mutex);
    
    cpu_job_slot_t* slot = NULL;
    for (int i = 0; i < 32; i++) {
        if (g_cpu_context.job_slots[i].active && 
            g_cpu_context.job_slots[i].job.job_id == job_id) {
            slot = &g_cpu_context.job_slots[i];
            break;
        }
    }
    
    if (!slot) {
        pthread_mutex_unlock(&g_cpu_context.mutex);
        return HAL_ERROR_INVALID_PARAM;
    }
    
    *result = slot->result;
    
    hal_error_t ret = (slot->result.status == HAL_STATUS_COMPLETED || 
                      slot->result.status == HAL_STATUS_ERROR ||
                      slot->result.status == HAL_STATUS_TIMEOUT) ? 
                      HAL_SUCCESS : HAL_ERROR_BUSY;
    
    pthread_mutex_unlock(&g_cpu_context.mutex);
    
    return ret;
}

hal_error_t hal_cpu_get_status(hal_lane_status_t* status) {
    if (!status) {
        return HAL_ERROR_INVALID_PARAM;
    }
    
    pthread_mutex_lock(&g_cpu_context.mutex);
    
    // Count active jobs
    uint32_t pending_jobs = 0;
    for (int i = 0; i < 32; i++) {
        if (g_cpu_context.job_slots[i].active) {
            pending_jobs++;
        }
    }
    
    status->lane = HAL_LANE_CPU;
    status->online = g_cpu_context.online;
    status->healthy = g_cpu_context.online;
    status->pending_jobs = pending_jobs;
    status->completed_jobs = g_cpu_context.jobs_completed;
    status->failed_jobs = g_cpu_context.jobs_failed;
    status->cpu_usage_percent = g_cpu_context.cpu_usage_percent;
    status->memory_usage_percent = 45;  // Simulated
    status->temperature_celsius = g_cpu_context.temperature_celsius;
    status->power_consumption_mw = 8000;  // 8W simulated
    status->total_execution_time_us = g_cpu_context.total_execution_time_us;
    
    pthread_mutex_unlock(&g_cpu_context.mutex);
    
    return HAL_SUCCESS;
}

/* Private implementation functions */

static void* cpu_job_worker(void* arg) {
    cpu_job_slot_t* slot = (cpu_job_slot_t*)arg;
    
    // Record start time
    clock_gettime(CLOCK_MONOTONIC, &slot->start_time);
    slot->result.status = HAL_STATUS_RUNNING;
    
    // Execute the job
    hal_error_t exec_result = cpu_execute_function(&slot->job, &slot->result);
    
    // Calculate execution time
    struct timespec end_time;
    clock_gettime(CLOCK_MONOTONIC, &end_time);
    
    uint64_t start_us = slot->start_time.tv_sec * 1000000 + slot->start_time.tv_nsec / 1000;
    uint64_t end_us = end_time.tv_sec * 1000000 + end_time.tv_nsec / 1000;
    slot->result.execution_time_us = end_us - start_us;
    
    // Check WCET violation
    if (slot->result.execution_time_us > slot->job.wcet_us) {
        slot->result.status = HAL_STATUS_ERROR;
        slot->result.error_code = HAL_ERROR_TIMEOUT;
        slot->result.error_message = "WCET violation";
    } else if (exec_result == HAL_SUCCESS) {
        slot->result.status = HAL_STATUS_COMPLETED;
        slot->result.error_code = HAL_SUCCESS;
    } else {
        slot->result.status = HAL_STATUS_ERROR;
        slot->result.error_code = exec_result;
        slot->result.error_message = "Execution failed";
    }
    
    // Update statistics
    pthread_mutex_lock(&g_cpu_context.mutex);
    g_cpu_context.total_execution_time_us += slot->result.execution_time_us;
    if (slot->result.status == HAL_STATUS_COMPLETED) {
        g_cpu_context.jobs_completed++;
    } else {
        g_cpu_context.jobs_failed++;
    }
    pthread_mutex_unlock(&g_cpu_context.mutex);
    
    return NULL;
}

static hal_error_t cpu_execute_function(const hal_job_t* job, hal_result_t* result) {
    // Simulate function execution based on function name
    if (!job->function_name) {
        return HAL_ERROR_INVALID_PARAM;
    }
    
    // Simulate computation delay
    usleep(job->wcet_us / 2);  // Use half of WCET for simulation
    
    // Generate deterministic output based on input
    if (job->output_data && job->output_size > 0) {
        // Simple hash-based output generation
        uint32_t hash = 0x12345678;
        const uint8_t* input = (const uint8_t*)job->input_data;
        
        for (size_t i = 0; i < job->input_size; i++) {
            hash = hash * 31 + input[i];
        }
        
        // Fill output buffer
        uint8_t* output = (uint8_t*)job->output_data;
        size_t bytes_to_write = job->output_size < sizeof(hash) ? job->output_size : sizeof(hash);
        
        memcpy(output, &hash, bytes_to_write);
        
        if (job->actual_output_size) {
            *job->actual_output_size = bytes_to_write;
        }
        
        // Calculate checksum
        result->checksum = cpu_calculate_checksum(job->output_data, bytes_to_write);
    }
    
    return HAL_SUCCESS;
}

static uint32_t cpu_calculate_checksum(const void* data, size_t size) {
    uint32_t checksum = 0;
    const uint8_t* bytes = (const uint8_t*)data;
    
    for (size_t i = 0; i < size; i++) {
        checksum = checksum * 31 + bytes[i];
    }
    
    return checksum;
}

static uint64_t cpu_get_time_us(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1000000 + ts.tv_nsec / 1000;
}

/* CPU-specific extensions */

hal_error_t hal_cpu_set_affinity(uint32_t core_mask) {
    // Implementation would set CPU affinity using sched_setaffinity
    // For simulation, just validate parameters
    if (core_mask == 0 || core_mask > 0xFF) {
        return HAL_ERROR_INVALID_PARAM;
    }
    
    return HAL_SUCCESS;
}

hal_error_t hal_cpu_get_cache_stats(uint32_t* l1_hits, uint32_t* l1_misses,
                                   uint32_t* l2_hits, uint32_t* l2_misses) {
    if (!l1_hits || !l1_misses || !l2_hits || !l2_misses) {
        return HAL_ERROR_INVALID_PARAM;
    }
    
    // Simulated cache statistics
    *l1_hits = 9500;
    *l1_misses = 500;
    *l2_hits = 450;
    *l2_misses = 50;
    
    return HAL_SUCCESS;
}