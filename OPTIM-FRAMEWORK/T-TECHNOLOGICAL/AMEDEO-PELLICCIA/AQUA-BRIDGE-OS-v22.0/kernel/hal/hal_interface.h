/**
 * @file hal_interface.h
 * @brief Hardware Abstraction Layer Interface for ACT
 * @version 22.0
 * @date 2025-08-28
 * 
 * Unified HAL interface for CPU, FPGA, and DSP compute lanes
 * Supports heterogeneous 2oo3 redundancy with deterministic execution
 */

#ifndef HAL_INTERFACE_H
#define HAL_INTERFACE_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* HAL Version and Compatibility */
#define HAL_VERSION_MAJOR 22
#define HAL_VERSION_MINOR 0
#define HAL_VERSION_PATCH 0

/* Compute Lane Types */
typedef enum {
    HAL_LANE_CPU = 0,
    HAL_LANE_FPGA = 1,
    HAL_LANE_DSP = 2,
    HAL_LANE_COUNT = 3
} hal_lane_t;

/* Job Priority Levels */
typedef enum {
    HAL_PRIORITY_EMERGENCY = 0,  ///< Emergency/safety-critical
    HAL_PRIORITY_HIGH = 1,       ///< High priority (DAL-A)
    HAL_PRIORITY_NORMAL = 2,     ///< Normal priority
    HAL_PRIORITY_LOW = 3,        ///< Low priority
    HAL_PRIORITY_BACKGROUND = 4  ///< Background tasks
} hal_priority_t;

/* Job Status */
typedef enum {
    HAL_STATUS_PENDING = 0,
    HAL_STATUS_RUNNING = 1,
    HAL_STATUS_COMPLETED = 2,
    HAL_STATUS_TIMEOUT = 3,
    HAL_STATUS_ERROR = 4,
    HAL_STATUS_CANCELLED = 5
} hal_status_t;

/* Error Codes */
typedef enum {
    HAL_SUCCESS = 0,
    HAL_ERROR_INVALID_PARAM = -1,
    HAL_ERROR_NO_MEMORY = -2,
    HAL_ERROR_TIMEOUT = -3,
    HAL_ERROR_HARDWARE = -4,
    HAL_ERROR_BUSY = -5,
    HAL_ERROR_NOT_SUPPORTED = -6,
    HAL_ERROR_LANE_OFFLINE = -7
} hal_error_t;

/* Forward Declarations */
typedef struct hal_job hal_job_t;
typedef struct hal_result hal_result_t;
typedef struct hal_config hal_config_t;

/* Job Descriptor */
struct hal_job {
    uint32_t job_id;
    hal_priority_t priority;
    uint32_t timeout_us;           ///< Timeout in microseconds
    uint32_t wcet_us;              ///< Worst Case Execution Time
    const char* function_name;     ///< Function to execute
    const void* input_data;        ///< Input buffer
    size_t input_size;             ///< Input buffer size
    void* output_data;             ///< Output buffer
    size_t output_size;            ///< Output buffer size
    size_t* actual_output_size;    ///< Actual output size (written)
    void* context;                 ///< User context
};

/* Execution Result */
struct hal_result {
    uint32_t job_id;
    hal_lane_t lane;
    hal_status_t status;
    uint32_t execution_time_us;
    uint32_t checksum;             ///< Output checksum for voter
    hal_error_t error_code;
    const char* error_message;
};

/* Lane Configuration */
struct hal_config {
    hal_lane_t lane;
    uint32_t max_concurrent_jobs;
    uint32_t queue_depth;
    bool wcet_monitoring;
    bool power_gating_enabled;
    uint32_t clock_frequency_mhz;
};

/* Core HAL Functions */

/**
 * @brief Initialize HAL subsystem
 * @return HAL_SUCCESS on success, error code otherwise
 */
hal_error_t hal_init(void);

/**
 * @brief Shutdown HAL subsystem
 * @return HAL_SUCCESS on success, error code otherwise
 */
hal_error_t hal_shutdown(void);

/**
 * @brief Configure compute lane
 * @param config Lane configuration
 * @return HAL_SUCCESS on success, error code otherwise
 */
hal_error_t hal_configure_lane(const hal_config_t* config);

/**
 * @brief Submit job to specific compute lane
 * @param lane Target compute lane
 * @param job Job descriptor
 * @return HAL_SUCCESS on success, error code otherwise
 */
hal_error_t hal_submit_job(hal_lane_t lane, const hal_job_t* job);

/**
 * @brief Submit job to all lanes for 2oo3 redundancy
 * @param job Job descriptor (will be copied for each lane)
 * @return HAL_SUCCESS on success, error code otherwise
 */
hal_error_t hal_submit_redundant_job(const hal_job_t* job);

/**
 * @brief Wait for job completion
 * @param lane Compute lane
 * @param job_id Job identifier
 * @param result Result structure (output)
 * @param timeout_us Timeout in microseconds
 * @return HAL_SUCCESS on success, error code otherwise
 */
hal_error_t hal_wait_job(hal_lane_t lane, uint32_t job_id, 
                        hal_result_t* result, uint32_t timeout_us);

/**
 * @brief Poll job status (non-blocking)
 * @param lane Compute lane
 * @param job_id Job identifier
 * @param result Result structure (output, may be partial)
 * @return HAL_SUCCESS if completed, HAL_STATUS_PENDING if running
 */
hal_error_t hal_poll_job(hal_lane_t lane, uint32_t job_id, hal_result_t* result);

/**
 * @brief Cancel running job
 * @param lane Compute lane
 * @param job_id Job identifier
 * @return HAL_SUCCESS on success, error code otherwise
 */
hal_error_t hal_cancel_job(hal_lane_t lane, uint32_t job_id);

/**
 * @brief Synchronization barrier across compute lanes
 * @param group_id Synchronization group identifier
 * @param timeout_us Timeout in microseconds
 * @return HAL_SUCCESS when all lanes reach barrier
 */
hal_error_t hal_barrier_sync(uint32_t group_id, uint32_t timeout_us);

/* Lane Status and Monitoring */

/**
 * @brief Get lane status and health
 * @param lane Compute lane
 * @param status Status structure (output)
 * @return HAL_SUCCESS on success, error code otherwise
 */
typedef struct {
    hal_lane_t lane;
    bool online;
    bool healthy;
    uint32_t pending_jobs;
    uint32_t completed_jobs;
    uint32_t failed_jobs;
    uint32_t cpu_usage_percent;
    uint32_t memory_usage_percent;
    uint32_t temperature_celsius;
    uint32_t power_consumption_mw;
    uint64_t total_execution_time_us;
} hal_lane_status_t;

hal_error_t hal_get_lane_status(hal_lane_t lane, hal_lane_status_t* status);

/**
 * @brief Get system-wide HAL statistics
 * @param stats Statistics structure (output)
 * @return HAL_SUCCESS on success, error code otherwise
 */
typedef struct {
    uint64_t total_jobs_submitted;
    uint64_t total_jobs_completed;
    uint64_t total_jobs_failed;
    uint32_t lanes_online;
    uint32_t lanes_healthy;
    uint64_t total_execution_time_us;
    uint32_t voter_unanimous_count;
    uint32_t voter_majority_count;
    uint32_t voter_split_count;
} hal_system_stats_t;

hal_error_t hal_get_system_stats(hal_system_stats_t* stats);

/* Power Management */

/**
 * @brief Set lane power state
 * @param lane Compute lane
 * @param power_state Power state (0=off, 1=standby, 2=active, 3=turbo)
 * @return HAL_SUCCESS on success, error code otherwise
 */
hal_error_t hal_set_power_state(hal_lane_t lane, uint32_t power_state);

/**
 * @brief Set lane clock frequency
 * @param lane Compute lane
 * @param frequency_mhz Clock frequency in MHz
 * @return HAL_SUCCESS on success, error code otherwise
 */
hal_error_t hal_set_clock_frequency(hal_lane_t lane, uint32_t frequency_mhz);

/* Debug and Diagnostics */

/**
 * @brief Run lane self-test
 * @param lane Compute lane
 * @param test_vector Test pattern
 * @param result Test result (output)
 * @return HAL_SUCCESS on success, error code otherwise
 */
typedef struct {
    bool passed;
    uint32_t test_duration_us;
    uint32_t errors_detected;
    char error_description[256];
} hal_test_result_t;

hal_error_t hal_run_self_test(hal_lane_t lane, uint32_t test_vector, 
                             hal_test_result_t* result);

/**
 * @brief Enable/disable lane tracing
 * @param lane Compute lane
 * @param enable Enable tracing
 * @return HAL_SUCCESS on success, error code otherwise
 */
hal_error_t hal_set_tracing(hal_lane_t lane, bool enable);

/* Callback Functions */

/**
 * @brief Job completion callback
 * @param result Job execution result
 * @param user_data User-provided data
 */
typedef void (*hal_job_callback_t)(const hal_result_t* result, void* user_data);

/**
 * @brief Register job completion callback
 * @param callback Callback function
 * @param user_data User data passed to callback
 * @return HAL_SUCCESS on success, error code otherwise
 */
hal_error_t hal_register_callback(hal_job_callback_t callback, void* user_data);

/* Lane-Specific Extensions */

/* CPU Lane Extensions */
hal_error_t hal_cpu_set_affinity(uint32_t core_mask);
hal_error_t hal_cpu_get_cache_stats(uint32_t* l1_hits, uint32_t* l1_misses, 
                                   uint32_t* l2_hits, uint32_t* l2_misses);

/* FPGA Lane Extensions */
hal_error_t hal_fpga_load_bitstream(const void* bitstream, size_t size);
hal_error_t hal_fpga_get_utilization(uint32_t* logic_percent, uint32_t* dsp_percent,
                                    uint32_t* bram_percent);

/* DSP Lane Extensions */
hal_error_t hal_dsp_set_vector_mode(bool enable);
hal_error_t hal_dsp_get_memory_bandwidth(uint32_t* read_mbps, uint32_t* write_mbps);

#ifdef __cplusplus
}
#endif

#endif /* HAL_INTERFACE_H */