// AMPEL360 Interactive Framework Index JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeTreeView();
    initializeDomains();
    initializeSearch();
    initializeAnimations();
});

// Navigation functionality
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const contentSections = document.querySelectorAll('.content-section');

    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const targetSection = this.getAttribute('data-section');
            
            // Remove active class from all nav items and content sections
            navItems.forEach(nav => nav.classList.remove('active'));
            contentSections.forEach(section => section.classList.remove('active'));
            
            // Add active class to clicked nav item and corresponding content section
            this.classList.add('active');
            document.getElementById(targetSection).classList.add('active');
        });
    });
}

// Tree view functionality
function initializeTreeView() {
    const expandableItems = document.querySelectorAll('.tree-folder.expandable');
    
    expandableItems.forEach(item => {
        item.addEventListener('click', function() {
            const target = this.getAttribute('data-target');
            const targetElement = document.getElementById(target);
            
            if (targetElement) {
                targetElement.classList.toggle('expanded');
                this.classList.toggle('expanded');
            }
        });
    });
    
    // Populate technological domains in tree view
    populateDomainsTree();
}

// Populate domains in tree structure
function populateDomainsTree() {
    const domainsTree = document.getElementById('domains-tree');
    const domains = getTechnologicalDomains();
    
    domains.forEach(domain => {
        const domainItem = document.createElement('div');
        domainItem.className = 'tree-item';
        domainItem.innerHTML = `
            <span class="tree-folder">
                <i class="fas fa-folder"></i> 
                <a href="./T-TECHNOLOGICAL/AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/${domain.id}/" 
                   style="color: inherit; text-decoration: none;">
                    ${domain.name}
                </a>
            </span>
        `;
        domainsTree.appendChild(domainItem);
    });
}

// Initialize technological domains grid
function initializeDomains() {
    const domainsGrid = document.getElementById('domainsGrid');
    const domains = getTechnologicalDomains();
    
    domains.forEach(domain => {
        const domainCard = createDomainCard(domain);
        domainsGrid.appendChild(domainCard);
    });
}

// Create domain card element
function createDomainCard(domain) {
    const card = document.createElement('div');
    card.className = 'domain-card';
    card.innerHTML = `
        <h3>
            <i class="${domain.icon}"></i>
            ${domain.name}
        </h3>
        <p>${domain.description}</p>
        <a href="./T-TECHNOLOGICAL/AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/${domain.id}/" 
           class="domain-link">
            Explore Domain →
        </a>
    `;
    
    // Add click handler for entire card
    card.addEventListener('click', function(e) {
        if (e.target.tagName !== 'A') {
            window.location.href = `./T-TECHNOLOGICAL/AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/${domain.id}/`;
        }
    });
    
    return card;
}

// Get technological domains data
function getTechnologicalDomains() {
    return [
        {
            id: 'A-ARCHITECTURE',
            name: 'A-ARCHITECTURES',
            description: 'System architectures, structural design, and integration frameworks.',
            icon: 'fas fa-building'
        },
        {
            id: 'M-MECHANICAL',
            name: 'M-MECHANICAL',
            description: 'Mechanical systems, components, and structural engineering.',
            icon: 'fas fa-cogs'
        },
        {
            id: 'E-ENVIRONMENTAL',
            name: 'E1-ENVIRONMENTAL',
            description: 'Environmental systems, climate control, and sustainability.',
            icon: 'fas fa-leaf'
        },
        {
            id: 'D-DIGITAL',
            name: 'D-DIGITAL',
            description: 'Digital systems, software architecture, and computing platforms.',
            icon: 'fas fa-microchip'
        },
        {
            id: 'E2-ENERGY',
            name: 'E2-ENERGY',
            description: 'Energy systems, power management, and hydrogen technology.',
            icon: 'fas fa-bolt'
        },
        {
            id: 'O-OPERATING_SYSTEMS',
            name: 'O-OPERATING_SYSTEMS',
            description: 'Operating systems, runtime environments, and system software.',
            icon: 'fas fa-desktop'
        },
        {
            id: 'P-PROPULSION',
            name: 'P-PROPULSION',
            description: 'Propulsion systems, engines, and thrust generation.',
            icon: 'fas fa-rocket'
        },
        {
            id: 'E3-ELECTRONICS',
            name: 'E3-ELECTRONICS',
            description: 'Electronic systems, circuits, and hardware components.',
            icon: 'fas fa-circuit-board'
        },
        {
            id: 'L-LOGISTICS',
            name: 'L1-LOGISTICS',
            description: 'Logistics, supply chain, and resource management.',
            icon: 'fas fa-truck'
        },
        {
            id: 'L2-LINKS',
            name: 'L2-LINKS',
            description: 'Communication links, networks, and data transmission.',
            icon: 'fas fa-link'
        },
        {
            id: 'I-INFRASTRUCTURES',
            name: 'I-INFRASTRUCTURES',
            description: 'Infrastructure systems, facilities, and support structures.',
            icon: 'fas fa-industry'
        },
        {
            id: 'C-CONTROL',
            name: 'C1-COMPUTING',
            description: 'Control systems, automation, and computing infrastructure.',
            icon: 'fas fa-server'
        },
        {
            id: 'C2-CRYOGENICS',
            name: 'C2-CRYOGENICS',
            description: 'Cryogenic systems, cooling, and low-temperature technology.',
            icon: 'fas fa-snowflake'
        },
        {
            id: 'I2-INTELLIGENCE',
            name: 'I2-INTELLIGENCE',
            description: 'Artificial intelligence, machine learning, and smart systems.',
            icon: 'fas fa-brain'
        },
        {
            id: 'A2-AIRPORTS',
            name: 'A2-AIRPORTS',
            description: 'Airport systems, ground support, and infrastructure.',
            icon: 'fas fa-plane-departure'
        }
    ];
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = createSearchResultsContainer();
    
    searchInput.parentNode.appendChild(searchResults);
    
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            hideSearchResults();
            return;
        }
        
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
    
    // Hide search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.parentNode.contains(e.target)) {
            hideSearchResults();
        }
    });
}

// Create search results container
function createSearchResultsContainer() {
    const container = document.createElement('div');
    container.className = 'search-results';
    container.id = 'searchResults';
    return container;
}

// Perform search and display results
function performSearch(query) {
    const results = getSearchResults(query);
    const searchResults = document.getElementById('searchResults');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="search-result-item">No results found</div>';
    } else {
        searchResults.innerHTML = results.map(result => 
            `<div class="search-result-item" onclick="navigateTo('${result.url}')">
                <div class="search-result-title">${result.title}</div>
                <div class="search-result-path">${result.path}</div>
            </div>`
        ).join('');
    }
    
    searchResults.style.display = 'block';
}

// Get search results
function getSearchResults(query) {
    const domains = getTechnologicalDomains();
    const searchItems = [
        // Framework sections
        { title: 'O-ORGANIZATIONAL', path: 'Framework > Organizational', url: './O-ORGANIZATIONAL/' },
        { title: 'P-PROCEDURAL', path: 'Framework > Procedural', url: './P-PROCEDURAL/' },
        { title: 'T-TECHNOLOGICAL', path: 'Framework > Technological', url: './T-TECHNOLOGICAL/' },
        { title: 'I-INTELLIGENT', path: 'Framework > Intelligent', url: './I-INTELLIGENT/' },
        { title: 'M-MACHINE', path: 'Framework > Machine', url: './M-MACHINE/' },
        { title: 'E-EXECUTING', path: 'Framework > Executing', url: './E-EXECUTING/' },
        
        // Documentation
        { title: 'Framework Overview', path: 'Documentation > Main README', url: './README.md' },
        { title: 'Technical Index', path: 'Documentation > Technical', url: './T-TECHNOLOGICAL/README.md' },
        { title: 'Systems Index', path: 'Documentation > Systems', url: './T-TECHNOLOGICAL/AMEDEO-PELLICCIA/INTEGRATED/README.md' },
        
        // Applications
        { title: 'Application Ecosystem', path: 'Applications > Main Hub', url: './I-.INTELLIGENT/app/' },
        { title: 'CQEA Applications', path: 'Applications > Quantum-Classical', url: './I-.INTELLIGENT/app/CQEA_Classical_Quantum-Extensible_Applications/' },
        
        // Tools
        { title: 'Validation Tools', path: 'Tools > Validation', url: '../tools/' },
        { title: 'Build System', path: 'Tools > Make', url: '../Makefile' },
        { title: 'Demo Script', path: 'Tools > Demo', url: '../ampel360_integrated_demo.py' },
        
        // Configuration
        { title: 'Main Configuration', path: 'Config > Main', url: '../ampel360-config.yaml' },
        { title: 'Program Configuration', path: 'Config > Program', url: './T-TECHNOLOGICAL/AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/ampel-config.yaml' },
        { title: 'Dependencies', path: 'Config > Requirements', url: '../requirements.txt' }
    ];
    
    // Add domains to search items
    domains.forEach(domain => {
        searchItems.push({
            title: domain.name,
            path: `Technological Domains > ${domain.name}`,
            url: `./T-TECHNOLOGICAL/AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/${domain.id}/`
        });
    });
    
    const lowerQuery = query.toLowerCase();
    return searchItems.filter(item => 
        item.title.toLowerCase().includes(lowerQuery) ||
        item.path.toLowerCase().includes(lowerQuery)
    ).slice(0, 8); // Limit to 8 results
}

// Hide search results
function hideSearchResults() {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.style.display = 'none';
    }
}

// Navigate to URL
function navigateTo(url) {
    window.location.href = url;
}

// Initialize animations
function initializeAnimations() {
    // Observe elements for animation on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationDelay = Math.random() * 0.5 + 's';
                entry.target.classList.add('animated');
            }
        });
    });
    
    // Observe cards for staggered animation
    document.querySelectorAll('.overview-card, .domain-card, .quick-access-card').forEach(card => {
        observer.observe(card);
    });
}

// Utility functions
function showLoading(container) {
    container.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
}

function hideLoading(container) {
    const loading = container.querySelector('.loading');
    if (loading) {
        loading.remove();
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('searchInput').focus();
    }
    
    // Escape to clear search
    if (e.key === 'Escape') {
        document.getElementById('searchInput').value = '';
        hideSearchResults();
    }
});

// Add smooth scrolling to internal links
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    }
});

// Console welcome message
console.log('%c🚀 AMPEL360 H₂-BWB-Q Interactive Framework Index', 'color: #3498db; font-size: 16px; font-weight: bold;');
console.log('%cFramework loaded successfully! Use Ctrl+K to search.', 'color: #27ae60; font-size: 12px;');