// main.js for 03_url_parameters

document.addEventListener('DOMContentLoaded', function() {
    // Save button functionality
    const saveButtons = document.querySelectorAll('.save-btn');
    
    saveButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.classList.contains('saved')) {
                this.classList.remove('saved');
                this.innerHTML = '<i class="far fa-bookmark"></i> Save';
            } else {
                this.classList.add('saved');
                this.innerHTML = '<i class="fas fa-bookmark"></i> Saved';
            }
        });
    });
    
    // Play button functionality
    const playButton = document.querySelector('.play-button');
    if (playButton) {
        playButton.addEventListener('click', function() {
            if (this.classList.contains('playing')) {
                this.classList.remove('playing');
                this.innerHTML = '<i class="fas fa-play"></i>';
            } else {
                this.classList.add('playing');
                this.innerHTML = '<i class="fas fa-pause"></i>';
            }
        });
    }
    
    // Subscribe button functionality
    const subscribeButtons = document.querySelectorAll('.subscribe-btn');
    
    subscribeButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.classList.contains('subscribed')) {
                this.classList.remove('subscribed');
                this.textContent = 'Subscribe';
                this.style.backgroundColor = '#ff0000';
            } else {
                this.classList.add('subscribed');
                this.textContent = 'Subscribed';
                this.style.backgroundColor = '#717171';
            }
        });
    });
    
    // Follow button functionality
    const followButtons = document.querySelectorAll('.follow-btn');
    
    followButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.classList.contains('following')) {
                this.classList.remove('following');
                this.textContent = 'Follow';
                this.style.backgroundColor = '#ff0000';
            } else {
                this.classList.add('following');
                this.textContent = 'Following';
                this.style.backgroundColor = '#717171';
            }
        });
    });
    
    // Tab switching functionality
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            tabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Hide all tab contents
            tabContents.forEach(content => content.classList.add('hidden'));
            
            // Show the selected tab content
            const tabId = this.getAttribute('data-tab');
            document.getElementById(`${tabId}-content`).classList.remove('hidden');
        });
    });
    
    // Search filter functionality
    const filters = document.querySelectorAll('.filter');
    const videoResults = document.getElementById('videos-results');
    const articleResults = document.getElementById('articles-results');
    
    filters.forEach(filter => {
        filter.addEventListener('click', function() {
            // Remove active class from all filters
            filters.forEach(f => f.classList.remove('active'));
            
            // Add active class to clicked filter
            this.classList.add('active');
            
            const filterType = this.getAttribute('data-filter');
            
            if (filterType === 'all') {
                if (videoResults) videoResults.style.display = 'block';
                if (articleResults) articleResults.style.display = 'block';
            } else if (filterType === 'videos') {
                if (videoResults) videoResults.style.display = 'block';
                if (articleResults) articleResults.style.display = 'none';
            } else if (filterType === 'articles') {
                if (videoResults) videoResults.style.display = 'none';
                if (articleResults) articleResults.style.display = 'block';
            }
        });
    });
});