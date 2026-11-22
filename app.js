// FestMatch - Campus Fest Discovery & ROI Engine for F&B Brands
// Main Application Controller & Reactive State

(function () {
  'use strict';

  // --- STATE ---
  const state = {
    fests: [...FESTS_DATA],
    filteredFests: [...FESTS_DATA],
    filters: {
      city: 'All',
      maxBudget: 500000,
      goal: 'All',
      minFootfall: 3000,
      search: '',
      sortBy: 'cpm_asc',
      activePreset: 'all'
    },
    shortlist: [], // Array of fest IDs (Max 3)
    lastBooking: null
  };

  // --- LOCAL STORAGE KEY ---
  const STORAGE_KEY = 'festmatch_shortlist_v1';

  // --- INITIALIZATION ---
  document.addEventListener('DOMContentLoaded', () => {
    loadShortlistFromStorage();
    initPresets();
    setupEventListeners();
    applyFiltersAndRender();
    refreshIcons();
  });

  function refreshIcons() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }
  }

  // --- STORAGE HELPERS ---
  function loadShortlistFromStorage() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed)) {
          // Verify they exist in FESTS_DATA and limit to 3
          state.shortlist = parsed.filter(id => FESTS_DATA.some(f => f.id === id)).slice(0, 3);
        }
      }
    } catch (e) {
      console.warn('Could not read shortlist from localStorage', e);
      state.shortlist = [];
    }
  }

  function saveShortlistToStorage() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state.shortlist));
    } catch (e) {
      console.warn('Could not save shortlist to localStorage', e);
    }
  }

  // --- FORMATTING HELPERS ---
  function formatINR(amount) {
    if (typeof amount !== 'number') return '₹0';
    return '₹' + amount.toLocaleString('en-IN');
  }

  function formatShortINR(amount) {
    if (typeof amount !== 'number') return '₹0';
    if (amount >= 100000) {
      const lakhs = (amount / 100000).toFixed(1).replace(/\.0$/, '');
      return `₹${lakhs} Lakh${parseFloat(lakhs) > 1 ? 's' : ''}`;
    }
    return '₹' + (amount / 1000).toFixed(0) + 'k';
  }

  function formatNumber(num) {
    if (typeof num !== 'number') return '0';
    return num.toLocaleString('en-IN');
  }

  // Calculate CPM (Cost per 1,000 students)
  function calculateCPM(packageAmount, footfall) {
    if (!footfall || footfall <= 0) return 0;
    return Math.round((packageAmount / footfall) * 1000);
  }

  // --- PRESET CHIPS ---
  function initPresets() {
    const container = document.getElementById('presetChipsContainer');
    if (!container) return;

    container.innerHTML = QUICK_PRESETS.map(p => `
      <button 
        type="button" 
        data-preset="${p.id}" 
        onclick="applyPreset('${p.id}')"
        class="preset-chip text-xs px-2.5 py-1 rounded-lg border font-medium transition-all ${
          state.filters.activePreset === p.id 
            ? 'bg-rose-600 text-white border-rose-600 shadow-sm' 
            : 'bg-white hover:bg-slate-100 text-slate-700 border-slate-200'
        }"
      >
        ${p.label}
      </button>
    `).join('');
  }

  window.applyPreset = function (presetId) {
    state.filters.activePreset = presetId;
    
    // Reset filters to defaults before applying specific preset criteria
    if (presetId === 'all') {
      state.filters.maxBudget = 500000;
      state.filters.minFootfall = 3000;
      state.filters.goal = 'All';
      state.filters.city = 'All';
      state.filters.search = '';
    } else if (presetId === 'budget_under_1L') {
      state.filters.maxBudget = 100000;
    } else if (presetId === 'mega_reach') {
      state.filters.minFootfall = 25000;
    } else if (presetId === 'best_cpm') {
      state.filters.sortBy = 'cpm_asc';
      state.filters.maxBudget = 500000;
    } else if (presetId === 'beverage_sampling') {
      state.filters.goal = 'Product Sampling';
    }

    syncFilterInputsToState();
    applyFiltersAndRender();
    updatePresetChipsUI();
  };

  function updatePresetChipsUI() {
    document.querySelectorAll('.preset-chip').forEach(btn => {
      const id = btn.getAttribute('data-preset');
      if (id === state.filters.activePreset) {
        btn.className = 'preset-chip text-xs px-2.5 py-1 rounded-lg border font-medium transition-all bg-rose-600 text-white border-rose-600 shadow-sm';
      } else {
        btn.className = 'preset-chip text-xs px-2.5 py-1 rounded-lg border font-medium transition-all bg-white hover:bg-slate-100 text-slate-700 border-slate-200';
      }
    });
  }

  // --- FILTER & EVENT LISTENERS ---
  function setupEventListeners() {
    // City Tabs
    const cityButtons = document.querySelectorAll('#cityTabs button');
    cityButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        cityButtons.forEach(b => {
          b.classList.remove('active', 'bg-white', 'text-slate-900', 'shadow-sm', 'border', 'border-slate-200/60');
          b.classList.add('text-slate-600');
        });
        btn.classList.add('active', 'bg-white', 'text-slate-900', 'shadow-sm', 'border', 'border-slate-200/60');
        btn.classList.remove('text-slate-600');

        state.filters.city = btn.getAttribute('data-city') || 'All';
        state.filters.activePreset = 'custom';
        updatePresetChipsUI();
        applyFiltersAndRender();
      });
    });

    // Budget Slider
    const budgetRange = document.getElementById('budgetRange');
    const budgetDisplay = document.getElementById('budgetValueDisplay');
    budgetRange.addEventListener('input', (e) => {
      const val = parseInt(e.target.value, 10);
      state.filters.maxBudget = val;
      state.filters.activePreset = 'custom';
      budgetDisplay.textContent = formatINR(val);
      updatePresetChipsUI();
      applyFiltersAndRender();
    });

    // Footfall Slider
    const footfallRange = document.getElementById('footfallRange');
    const footfallDisplay = document.getElementById('footfallValueDisplay');
    footfallRange.addEventListener('input', (e) => {
      const val = parseInt(e.target.value, 10);
      state.filters.minFootfall = val;
      state.filters.activePreset = 'custom';
      footfallDisplay.textContent = val <= 3000 ? 'Any Footfall' : `${formatNumber(val)}+ Students`;
      updatePresetChipsUI();
      applyFiltersAndRender();
    });

    // Campaign Goal Filter
    const goalFilter = document.getElementById('goalFilter');
    goalFilter.addEventListener('change', (e) => {
      state.filters.goal = e.target.value;
      state.filters.activePreset = 'custom';
      updatePresetChipsUI();
      applyFiltersAndRender();
    });

    // Sort Dropdown
    const sortSelect = document.getElementById('sortSelect');
    sortSelect.addEventListener('change', (e) => {
      state.filters.sortBy = e.target.value;
      applyFiltersAndRender();
    });

    // Search Input
    const searchInput = document.getElementById('searchInput');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    searchInput.addEventListener('input', (e) => {
      state.filters.search = e.target.value.trim().toLowerCase();
      if (state.filters.search) {
        clearSearchBtn.classList.remove('hidden');
      } else {
        clearSearchBtn.classList.add('hidden');
      }
      applyFiltersAndRender();
    });

    clearSearchBtn.addEventListener('click', () => {
      searchInput.value = '';
      state.filters.search = '';
      clearSearchBtn.classList.add('hidden');
      applyFiltersAndRender();
    });

    // Keyboard escape to close open modals
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeComparisonModal();
        closePitchModal();
        closeFestDetailModal();
        closeAboutModal();
      }
    });
  }

  function syncFilterInputsToState() {
    const budgetRange = document.getElementById('budgetRange');
    const budgetDisplay = document.getElementById('budgetValueDisplay');
    budgetRange.value = state.filters.maxBudget;
    budgetDisplay.textContent = formatINR(state.filters.maxBudget);

    const footfallRange = document.getElementById('footfallRange');
    const footfallDisplay = document.getElementById('footfallValueDisplay');
    footfallRange.value = state.filters.minFootfall;
    footfallDisplay.textContent = state.filters.minFootfall <= 3000 ? 'Any Footfall' : `${formatNumber(state.filters.minFootfall)}+ Students`;

    const goalFilter = document.getElementById('goalFilter');
    goalFilter.value = state.filters.goal;

    const sortSelect = document.getElementById('sortSelect');
    sortSelect.value = state.filters.sortBy;

    const searchInput = document.getElementById('searchInput');
    searchInput.value = state.filters.search;

    // Sync city tab buttons
    const cityButtons = document.querySelectorAll('#cityTabs button');
    cityButtons.forEach(btn => {
      const city = btn.getAttribute('data-city');
      if (city === state.filters.city) {
        btn.classList.add('active', 'bg-white', 'text-slate-900', 'shadow-sm', 'border', 'border-slate-200/60');
        btn.classList.remove('text-slate-600');
      } else {
        btn.classList.remove('active', 'bg-white', 'text-slate-900', 'shadow-sm', 'border', 'border-slate-200/60');
        btn.classList.add('text-slate-600');
      }
    });
  }

  window.resetAllFilters = function () {
    state.filters = {
      city: 'All',
      maxBudget: 500000,
      goal: 'All',
      minFootfall: 3000,
      search: '',
      sortBy: 'cpm_asc',
      activePreset: 'all'
    };
    syncFilterInputsToState();
    updatePresetChipsUI();
    applyFiltersAndRender();
    showToast('Filters reset to default', 'info');
  };

  // --- FILTERING & SORTING LOGIC ---
  function applyFiltersAndRender() {
    const { city, maxBudget, goal, minFootfall, search, sortBy } = state.filters;

    let result = state.fests.filter(fest => {
      // City check
      if (city !== 'All' && fest.city.toLowerCase() !== city.toLowerCase()) {
        return false;
      }

      // Max Budget check
      if (fest.startingPackage > maxBudget) {
        return false;
      }

      // Min Footfall check
      if (fest.footfall < minFootfall) {
        return false;
      }

      // Goal check
      if (goal !== 'All') {
        const hasGoal = fest.supportedGoals.some(g => g.toLowerCase() === goal.toLowerCase());
        if (!hasGoal) return false;
      }

      // Search keyword check
      if (search) {
        const query = search.toLowerCase();
        const matchName = fest.name.toLowerCase().includes(query);
        const matchCollege = fest.college.toLowerCase().includes(query);
        const matchCity = fest.city.toLowerCase().includes(query);
        const matchVibe = fest.vibeTag.toLowerCase().includes(query);
        if (!matchName && !matchCollege && !matchCity && !matchVibe) {
          return false;
        }
      }

      return true;
    });

    // Sorting
    result.sort((a, b) => {
      const cpmA = calculateCPM(a.startingPackage, a.footfall);
      const cpmB = calculateCPM(b.startingPackage, b.footfall);

      if (sortBy === 'cpm_asc') return cpmA - cpmB;
      if (sortBy === 'footfall_desc') return b.footfall - a.footfall;
      if (sortBy === 'budget_asc') return a.startingPackage - b.startingPackage;
      if (sortBy === 'budget_desc') return b.startingPackage - a.startingPackage;
      return 0;
    });

    state.filteredFests = result;
    renderCards(result);
    renderShortlistBar();

    // Update filter status counters
    const resultsCountEl = document.getElementById('resultsCount');
    if (resultsCountEl) resultsCountEl.textContent = result.length;

    const filterActiveBadge = document.getElementById('filterActiveBadge');
    const isFiltered = city !== 'All' || maxBudget < 500000 || minFootfall > 3000 || goal !== 'All' || search !== '';
    if (filterActiveBadge) {
      filterActiveBadge.classList.toggle('hidden', !isFiltered);
    }

    const emptyState = document.getElementById('emptyState');
    const festsGrid = document.getElementById('festsGrid');
    if (result.length === 0) {
      emptyState.classList.remove('hidden');
      festsGrid.classList.add('hidden');
    } else {
      emptyState.classList.add('hidden');
      festsGrid.classList.remove('hidden');
    }

    refreshIcons();
  }

  // --- RENDER CARDS ---
  function renderCards(fests) {
    const grid = document.getElementById('festsGrid');
    if (!grid) return;

    grid.innerHTML = fests.map(fest => {
      const isShortlisted = state.shortlist.includes(fest.id);
      const cpm = calculateCPM(fest.startingPackage, fest.footfall);
      
      // Determine CPM Value badge
      let cpmBadgeColor = 'bg-emerald-50 text-emerald-700 border-emerald-200';
      let cpmLabel = 'High ROI Value';
      if (cpm > 6500) {
        cpmBadgeColor = 'bg-purple-50 text-purple-700 border-purple-200';
        cpmLabel = 'Flagship Reach';
      } else if (cpm > 5000) {
        cpmBadgeColor = 'bg-blue-50 text-blue-700 border-blue-200';
        cpmLabel = 'Standard Tier';
      }

      return `
        <article class="fest-card bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden flex flex-col ${isShortlisted ? 'is-shortlisted ring-2 ring-rose-500' : ''}">
          
          <!-- Card Header Banner with gradient & tags -->
          <div class="relative bg-gradient-to-r ${fest.bgGradient} p-4 text-white">
            <div class="flex items-center justify-between gap-2 mb-2">
              <span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-white/20 backdrop-blur-md text-white border border-white/20">
                ${fest.coverTag} • ${fest.edition}
              </span>
              <span class="inline-flex items-center gap-1 text-[11px] font-semibold bg-black/30 backdrop-blur-md px-2 py-0.5 rounded-full border border-white/10">
                <i data-lucide="map-pin" class="w-3 h-3 text-rose-300"></i> ${fest.campusArea}
              </span>
            </div>

            <h3 class="text-xl font-extrabold tracking-tight text-white flex items-center justify-between">
              <span>${fest.name}</span>
              ${fest.verified ? `
                <span class="inline-flex items-center gap-1 text-[10px] font-bold bg-emerald-500/90 text-white px-2 py-0.5 rounded-full border border-emerald-400 shadow-sm" title="Verified College Footfall Audit">
                  <i data-lucide="check-check" class="w-3 h-3"></i> Verified
                </span>
              ` : ''}
            </h3>

            <div class="text-xs text-slate-100 font-medium mt-0.5 flex items-center gap-1">
              <span>${fest.college}</span>
            </div>

            <div class="mt-2.5 flex items-center gap-2 text-[11px] text-white/90">
              <span class="flex items-center gap-1">
                <i data-lucide="calendar" class="w-3.5 h-3.5 text-amber-300"></i> ${fest.dates}
              </span>
              <span class="text-white/40">•</span>
              <span>${fest.daysCount} Days</span>
            </div>
          </div>

          <!-- Card Body: Metrics & Crowd Vibe -->
          <div class="p-5 flex-1 flex flex-col justify-between space-y-4">
            
            <!-- Crowd / Vibe Tag -->
            <div class="bg-slate-50 border border-slate-200/80 rounded-xl p-2.5">
              <div class="text-[10px] uppercase font-bold text-slate-500 tracking-wider mb-0.5">Audience & Campus Vibe</div>
              <div class="text-xs font-semibold text-slate-800 flex items-start gap-1.5">
                <i data-lucide="sparkles" class="w-3.5 h-3.5 text-rose-600 mt-0.5 shrink-0"></i>
                <span>${fest.vibeTag}</span>
              </div>
            </div>

            <!-- Standardized Decision Metrics Grid -->
            <div class="grid grid-cols-3 gap-2 bg-slate-50/70 p-3 rounded-xl border border-slate-100 text-center">
              
              <!-- Metric 1: Footfall -->
              <div class="space-y-0.5">
                <div class="text-[10px] text-slate-500 font-medium flex items-center justify-center gap-0.5">
                  <i data-lucide="users" class="w-3 h-3 text-slate-400"></i> Reach
                </div>
                <div class="text-sm font-extrabold text-slate-900 font-mono-numbers">
                  ${formatNumber(fest.footfall)}
                </div>
                <div class="text-[9px] text-slate-500">Students</div>
              </div>

              <!-- Metric 2: Starting Package -->
              <div class="space-y-0.5 border-x border-slate-200/60 px-1">
                <div class="text-[10px] text-slate-500 font-medium flex items-center justify-center gap-0.5">
                  <i data-lucide="banknote" class="w-3 h-3 text-slate-400"></i> Package
                </div>
                <div class="text-sm font-extrabold text-rose-700 font-mono-numbers">
                  ${formatShortINR(fest.startingPackage)}
                </div>
                <div class="text-[9px] text-slate-500">${formatINR(fest.startingPackage)}</div>
              </div>

              <!-- Metric 3: Auto-calculated CPM -->
              <div class="space-y-0.5">
                <div class="text-[10px] text-slate-500 font-medium flex items-center justify-center gap-0.5">
                  <i data-lucide="gauge" class="w-3 h-3 text-slate-400"></i> Cost / 1k
                </div>
                <div class="text-sm font-extrabold text-emerald-700 font-mono-numbers">
                  ₹${cpm.toLocaleString('en-IN')}
                </div>
                <div class="text-[9px] font-semibold text-emerald-600">Per 1,000</div>
              </div>

            </div>

            <!-- Campaign Goals Chips -->
            <div>
              <div class="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">Supported Activations</div>
              <div class="flex flex-wrap gap-1">
                ${fest.supportedGoals.map(goal => `
                  <span class="inline-flex items-center text-[10px] font-medium px-2 py-0.5 rounded-md ${
                    goal === 'Product Sampling' 
                      ? 'bg-amber-50 text-amber-800 border border-amber-200' 
                      : goal === 'Food Stall'
                      ? 'bg-rose-50 text-rose-800 border border-rose-200'
                      : 'bg-indigo-50 text-indigo-800 border border-indigo-200'
                  }">
                    ${goal === 'Product Sampling' ? '🥤' : goal === 'Food Stall' ? '🍔' : '⭐'} ${goal}
                  </span>
                `).join('')}
              </div>
            </div>

            <!-- Card Actions -->
            <div class="pt-3 border-t border-slate-100 flex items-center gap-2">
              <button 
                type="button"
                onclick="openFestDetailModal('${fest.id}')" 
                class="flex-1 py-2 px-3 text-xs font-semibold text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors flex items-center justify-center gap-1"
              >
                <i data-lucide="eye" class="w-3.5 h-3.5"></i> F&B Specs
              </button>

              <button 
                type="button"
                onclick="toggleShortlist('${fest.id}')" 
                class="flex-1 py-2 px-3 text-xs font-bold rounded-xl transition-all shadow-sm flex items-center justify-center gap-1.5 ${
                  isShortlisted 
                    ? 'bg-rose-100 hover:bg-rose-200 text-rose-800 border border-rose-300' 
                    : 'bg-rose-600 hover:bg-rose-700 text-white'
                }"
              >
                <i data-lucide="${isShortlisted ? 'check' : 'plus'}" class="w-3.5 h-3.5"></i>
                <span>${isShortlisted ? 'Shortlisted' : 'Shortlist'}</span>
              </button>
            </div>

          </div>

        </article>
      `;
    }).join('');
  }

  // --- SHORTLIST OPERATIONS (MAX 3) ---
  window.toggleShortlist = function (festId) {
    const fest = FESTS_DATA.find(f => f.id === festId);
    if (!fest) return;

    const index = state.shortlist.indexOf(festId);

    if (index > -1) {
      // Remove from shortlist
      state.shortlist.splice(index, 1);
      saveShortlistToStorage();
      showToast(`Removed "${fest.name}" from shortlist`, 'info');
    } else {
      // Check maximum 3 limit
      if (state.shortlist.length >= 3) {
        showToast('Shortlist limit reached! You can shortlist up to 3 fests at a time.', 'warning');
        return;
      }
      state.shortlist.push(festId);
      saveShortlistToStorage();
      showToast(`Added "${fest.name}" to shortlist (${state.shortlist.length}/3)`, 'success');
    }

    applyFiltersAndRender();
  };

  window.removeFromShortlist = function (festId, fromComparisonModal = false) {
    const index = state.shortlist.indexOf(festId);
    if (index > -1) {
      state.shortlist.splice(index, 1);
      saveShortlistToStorage();
      applyFiltersAndRender();
      showToast('Removed from shortlist', 'info');
      if (fromComparisonModal) {
        if (state.shortlist.length === 0) {
          closeComparisonModal();
        } else {
          openComparisonModal();
        }
      }
    }
  };

  // --- RENDER FLOATING SHORTLIST BAR ---
  function renderShortlistBar() {
    const floatingBar = document.getElementById('shortlistFloatingBar');
    const navShortlistCount = document.getElementById('navShortlistCount');
    const badgeCount = document.getElementById('shortlistBadgeCount');
    const namesPreview = document.getElementById('shortlistFestNamesPreview');
    const thumbnailsContainer = document.getElementById('shortlistThumbnails');
    const totalReachEl = document.getElementById('shortlistTotalReach');
    const totalBudgetEl = document.getElementById('shortlistTotalBudget');
    const blendedCpmEl = document.getElementById('shortlistBlendedCpm');

    const count = state.shortlist.length;
    navShortlistCount.textContent = count;

    if (count === 0) {
      floatingBar.classList.add('hidden');
      return;
    }

    floatingBar.classList.remove('hidden');
    badgeCount.textContent = count;

    // Retrieve full objects for shortlisted fests
    const shortlistedFests = state.shortlist.map(id => FESTS_DATA.find(f => f.id === id)).filter(Boolean);

    // Compute aggregate reach and budget
    const totalReach = shortlistedFests.reduce((sum, f) => sum + f.footfall, 0);
    const totalBudget = shortlistedFests.reduce((sum, f) => sum + f.startingPackage, 0);
    const blendedCPM = totalReach > 0 ? Math.round((totalBudget / totalReach) * 1000) : 0;

    totalReachEl.textContent = `${formatNumber(totalReach)} Students`;
    totalBudgetEl.textContent = formatINR(totalBudget);
    blendedCpmEl.textContent = `₹${blendedCPM.toLocaleString('en-IN')}`;

    // Names preview
    namesPreview.textContent = shortlistedFests.map(f => f.name).join(' • ');

    // Thumbnails / Chips
    thumbnailsContainer.innerHTML = shortlistedFests.map(fest => `
      <div class="inline-flex items-center gap-1.5 bg-slate-800 border border-slate-700 rounded-lg px-2 py-1 text-xs text-white">
        <span class="font-semibold text-rose-300">${fest.name}</span>
        <button onclick="removeFromShortlist('${fest.id}')" class="text-slate-400 hover:text-white" title="Remove ${fest.name}">
          <i data-lucide="x" class="w-3 h-3"></i>
        </button>
      </div>
    `).join('');
  }

  // --- SIDE-BY-SIDE COMPARISON MODAL ---
  window.openComparisonModal = function () {
    const modal = document.getElementById('comparisonModal');
    const container = document.getElementById('comparisonTableContainer');
    const countEl = document.getElementById('comparisonModalCount');

    if (state.shortlist.length === 0) {
      showToast('Please shortlist at least 1 fest to compare', 'warning');
      return;
    }

    countEl.textContent = `${state.shortlist.length} of 3 Selected`;

    const shortlistedFests = state.shortlist.map(id => FESTS_DATA.find(f => f.id === id)).filter(Boolean);

    // Build side-by-side comparison matrix table
    container.innerHTML = `
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="border-b border-slate-200">
              <th class="p-3 text-slate-500 font-bold uppercase tracking-wider w-48 bg-slate-50">Metric / Fest</th>
              ${shortlistedFests.map(f => `
                <th class="p-3 bg-slate-50 border-l border-slate-200">
                  <div class="flex items-start justify-between gap-2">
                    <div>
                      <div class="text-sm font-extrabold text-slate-900">${f.name}</div>
                      <div class="text-[11px] font-medium text-slate-500">${f.college} • ${f.city}</div>
                    </div>
                    <button onclick="removeFromShortlist('${f.id}', true);" class="text-slate-400 hover:text-rose-600 p-1" title="Remove">
                      <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                    </button>
                  </div>
                </th>
              `).join('')}
              ${[...Array(3 - shortlistedFests.length)].map((_, idx) => `
                <th class="p-4 bg-slate-50/50 border-l border-dashed border-slate-200 text-center text-slate-400 font-normal">
                  <div class="py-4">
                    <i data-lucide="plus-circle" class="w-5 h-5 mx-auto mb-1 text-slate-300"></i>
                    <span>Slot Available (${shortlistedFests.length + idx + 1}/3)</span>
                  </div>
                </th>
              `).join('')}
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr>
              <td class="p-3 font-semibold text-slate-600 bg-slate-50/60">Verified Footfall</td>
              ${shortlistedFests.map(f => `
                <td class="p-3 border-l border-slate-200 font-mono font-bold text-slate-900">
                  ${formatNumber(f.footfall)} Students
                </td>
              `).join('')}
              ${[...Array(3 - shortlistedFests.length)].map(() => `<td class="p-3 border-l border-dashed border-slate-200 text-slate-300">-</td>`).join('')}
            </tr>
            <tr>
              <td class="p-3 font-semibold text-slate-600 bg-slate-50/60">Starting Package</td>
              ${shortlistedFests.map(f => `
                <td class="p-3 border-l border-slate-200 font-mono font-bold text-rose-700">
                  ${formatINR(f.startingPackage)}
                </td>
              `).join('')}
              ${[...Array(3 - shortlistedFests.length)].map(() => `<td class="p-3 border-l border-dashed border-slate-200 text-slate-300">-</td>`).join('')}
            </tr>
            <tr>
              <td class="p-3 font-semibold text-slate-600 bg-slate-50/60">Cost per 1k Students (CPM)</td>
              ${shortlistedFests.map(f => `
                <td class="p-3 border-l border-slate-200 font-mono font-bold text-emerald-700">
                  ₹${calculateCPM(f.startingPackage, f.footfall).toLocaleString('en-IN')}
                </td>
              `).join('')}
              ${[...Array(3 - shortlistedFests.length)].map(() => `<td class="p-3 border-l border-dashed border-slate-200 text-slate-300">-</td>`).join('')}
            </tr>
            <tr>
              <td class="p-3 font-semibold text-slate-600 bg-slate-50/60">Dates & Duration</td>
              ${shortlistedFests.map(f => `
                <td class="p-3 border-l border-slate-200 text-slate-700">
                  ${f.dates} (${f.daysCount} Days)
                </td>
              `).join('')}
              ${[...Array(3 - shortlistedFests.length)].map(() => `<td class="p-3 border-l border-dashed border-slate-200 text-slate-300">-</td>`).join('')}
            </tr>
            <tr>
              <td class="p-3 font-semibold text-slate-600 bg-slate-50/60">Campus Crowd & Vibe</td>
              ${shortlistedFests.map(f => `
                <td class="p-3 border-l border-slate-200 text-slate-800">
                  ${f.vibeTag}
                </td>
              `).join('')}
              ${[...Array(3 - shortlistedFests.length)].map(() => `<td class="p-3 border-l border-dashed border-slate-200 text-slate-300">-</td>`).join('')}
            </tr>
            <tr>
              <td class="p-3 font-semibold text-slate-600 bg-slate-50/60">Chiller Power & Freezers</td>
              ${shortlistedFests.map(f => `
                <td class="p-3 border-l border-slate-200 text-slate-700 font-medium">
                  ${f.specs.chillerPower}
                </td>
              `).join('')}
              ${[...Array(3 - shortlistedFests.length)].map(() => `<td class="p-3 border-l border-dashed border-slate-200 text-slate-300">-</td>`).join('')}
            </tr>
            <tr>
              <td class="p-3 font-semibold text-slate-600 bg-slate-50/60">Sampling Permissions</td>
              ${shortlistedFests.map(f => `
                <td class="p-3 border-l border-slate-200 text-slate-700">
                  ${f.specs.samplingPermissions}
                </td>
              `).join('')}
              ${[...Array(3 - shortlistedFests.length)].map(() => `<td class="p-3 border-l border-dashed border-slate-200 text-slate-300">-</td>`).join('')}
            </tr>
            <tr>
              <td class="p-3 font-semibold text-slate-600 bg-slate-50/60">Peak Consumption Hours</td>
              ${shortlistedFests.map(f => `
                <td class="p-3 border-l border-slate-200 text-slate-700">
                  ${f.specs.peakHours}
                </td>
              `).join('')}
              ${[...Array(3 - shortlistedFests.length)].map(() => `<td class="p-3 border-l border-dashed border-slate-200 text-slate-300">-</td>`).join('')}
            </tr>
            <tr>
              <td class="p-3 font-semibold text-slate-600 bg-slate-50/60">Best Brand Fit Verdict</td>
              ${shortlistedFests.map(f => `
                <td class="p-3 border-l border-slate-200 text-rose-800 font-semibold bg-rose-50/50">
                  ${f.specs.fnbFitVerdict}
                </td>
              `).join('')}
              ${[...Array(3 - shortlistedFests.length)].map(() => `<td class="p-3 border-l border-dashed border-slate-200 text-slate-300">-</td>`).join('')}
            </tr>
          </tbody>
        </table>
      </div>
    `;

    modal.classList.remove('hidden');
    refreshIcons();
  };

  window.closeComparisonModal = function () {
    const modal = document.getElementById('comparisonModal');
    if (modal) modal.classList.add('hidden');
  };

  // --- FEST DETAIL & F&B SPECS MODAL ---
  window.openFestDetailModal = function (festId) {
    const fest = FESTS_DATA.find(f => f.id === festId);
    if (!fest) return;

    const modal = document.getElementById('festDetailModal');
    const content = document.getElementById('festDetailContent');
    const cpm = calculateCPM(fest.startingPackage, fest.footfall);
    const isShortlisted = state.shortlist.includes(fest.id);

    content.innerHTML = `
      <div class="relative bg-gradient-to-r ${fest.bgGradient} p-6 text-white">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-bold uppercase tracking-wider bg-white/20 backdrop-blur-sm px-2.5 py-0.5 rounded text-white border border-white/20">
            ${fest.coverTag} • ${fest.edition}
          </span>
          <button onclick="closeFestDetailModal()" class="w-8 h-8 rounded-full bg-black/30 hover:bg-black/50 text-white flex items-center justify-center transition-colors">
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>
        <h2 class="text-2xl font-black text-white">${fest.name}</h2>
        <p class="text-sm text-slate-100 font-medium">${fest.college} • ${fest.campusArea}</p>
        <div class="mt-3 flex flex-wrap items-center gap-3 text-xs text-white/90">
          <span class="flex items-center gap-1"><i data-lucide="calendar" class="w-3.5 h-3.5 text-amber-300"></i> ${fest.dates}</span>
          <span>•</span>
          <span class="flex items-center gap-1"><i data-lucide="users" class="w-3.5 h-3.5 text-indigo-300"></i> ${formatNumber(fest.footfall)} Verified Footfall</span>
        </div>
      </div>

      <div class="p-6 space-y-5 max-h-[70vh] overflow-y-auto text-xs">
        <!-- Overview -->
        <div>
          <h4 class="font-bold text-slate-900 uppercase tracking-wider text-[11px] mb-1">Campus Profile</h4>
          <p class="text-slate-600 leading-relaxed">${fest.description}</p>
        </div>

        <!-- Decision Math Box -->
        <div class="grid grid-cols-3 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-200 text-center">
          <div>
            <div class="text-[10px] text-slate-500 font-medium">Starting Package</div>
            <div class="text-base font-extrabold text-rose-700 font-mono-numbers mt-0.5">${formatINR(fest.startingPackage)}</div>
          </div>
          <div class="border-x border-slate-200">
            <div class="text-[10px] text-slate-500 font-medium">Verified Footfall</div>
            <div class="text-base font-extrabold text-slate-900 font-mono-numbers mt-0.5">${formatNumber(fest.footfall)}</div>
          </div>
          <div>
            <div class="text-[10px] text-slate-500 font-medium">Cost / 1k Students</div>
            <div class="text-base font-extrabold text-emerald-700 font-mono-numbers mt-0.5">₹${cpm.toLocaleString('en-IN')}</div>
          </div>
        </div>

        <!-- F&B Logistics Specifications -->
        <div class="space-y-3">
          <h4 class="font-bold text-slate-900 uppercase tracking-wider text-[11px]">F&B Brand Logistics & Permissions</h4>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span class="font-semibold text-slate-800 flex items-center gap-1.5 mb-1">
                <i data-lucide="zap" class="w-3.5 h-3.5 text-amber-500"></i> Chiller & Freezer Power
              </span>
              <p class="text-slate-600">${fest.specs.chillerPower}</p>
            </div>
            <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span class="font-semibold text-slate-800 flex items-center gap-1.5 mb-1">
                <i data-lucide="store" class="w-3.5 h-3.5 text-rose-500"></i> Stall Dimensions
              </span>
              <p class="text-slate-600">${fest.specs.stallDimensions}</p>
            </div>
            <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span class="font-semibold text-slate-800 flex items-center gap-1.5 mb-1">
                <i data-lucide="clock" class="w-3.5 h-3.5 text-indigo-500"></i> Peak Consumption Rush
              </span>
              <p class="text-slate-600">${fest.specs.peakHours}</p>
            </div>
            <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span class="font-semibold text-slate-800 flex items-center gap-1.5 mb-1">
                <i data-lucide="badge-check" class="w-3.5 h-3.5 text-emerald-500"></i> Commercial Sales
              </span>
              <p class="text-slate-600">${fest.specs.commercialSales}</p>
            </div>
          </div>
        </div>

        <!-- Demographics & Past Sponsors -->
        <div class="p-4 bg-rose-50/60 rounded-xl border border-rose-100 space-y-2">
          <div>
            <span class="font-bold text-rose-900">Demographic Profile:</span>
            <span class="text-slate-700 ml-1">${fest.specs.studentDemographics}</span>
          </div>
          <div>
            <span class="font-bold text-rose-900">Past F&B Brands at Fest:</span>
            <div class="flex flex-wrap gap-1.5 mt-1">
              ${fest.specs.pastFnbBrands.map(b => `<span class="bg-white px-2 py-0.5 rounded text-[10px] font-semibold text-slate-800 border border-rose-200 shadow-2xs">${b}</span>`).join('')}
            </div>
          </div>
        </div>
      </div>

      <!-- Footer CTA -->
      <div class="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
        <button onclick="closeFestDetailModal()" class="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-800 rounded-xl hover:bg-slate-200 transition-colors">
          Close
        </button>
        <button 
          onclick="toggleShortlist('${fest.id}'); closeFestDetailModal();" 
          class="px-4 py-2 text-xs font-bold rounded-xl transition-all shadow-sm flex items-center gap-1.5 ${
            isShortlisted ? 'bg-slate-200 text-slate-700' : 'bg-rose-600 hover:bg-rose-700 text-white'
          }"
        >
          <i data-lucide="${isShortlisted ? 'check' : 'plus'}" class="w-3.5 h-3.5"></i>
          <span>${isShortlisted ? 'Shortlisted' : 'Add to Shortlist'}</span>
        </button>
      </div>
    `;

    modal.classList.remove('hidden');
    refreshIcons();
  };

  window.closeFestDetailModal = function () {
    const modal = document.getElementById('festDetailModal');
    if (modal) modal.classList.add('hidden');
  };

  // --- PITCH CALL BOOKING MODAL & WORKFLOW ---
  window.openPitchCallModal = function () {
    if (state.shortlist.length === 0) {
      showToast('Please shortlist at least 1 fest first', 'warning');
      return;
    }

    const modal = document.getElementById('pitchModal');
    const formContainer = document.getElementById('pitchFormContainer');
    const successContainer = document.getElementById('pitchSuccessContainer');
    const tagsContainer = document.getElementById('pitchSelectedFestsTags');
    const reachSummary = document.getElementById('pitchModalReachSummary');

    // Show form view, hide success view
    formContainer.classList.remove('hidden');
    successContainer.classList.add('hidden');

    const shortlistedFests = state.shortlist.map(id => FESTS_DATA.find(f => f.id === id)).filter(Boolean);
    const totalReach = shortlistedFests.reduce((sum, f) => sum + f.footfall, 0);

    reachSummary.textContent = `Est. Reach: ${formatNumber(totalReach)} Students`;

    tagsContainer.innerHTML = shortlistedFests.map(f => `
      <span class="inline-flex items-center gap-1 text-[11px] font-semibold bg-white text-rose-800 px-2 py-0.5 rounded-md border border-rose-200">
        <i data-lucide="check" class="w-3 h-3 text-rose-600"></i> ${f.name} (${f.college})
      </span>
    `).join('');

    modal.classList.remove('hidden');
    refreshIcons();
  };

  window.closePitchModal = function () {
    const modal = document.getElementById('pitchModal');
    if (modal) modal.classList.add('hidden');
  };

  window.handlePitchFormSubmit = function (event) {
    event.preventDefault();

    const brandName = document.getElementById('brandNameInput').value.trim();
    const brandCategory = document.getElementById('brandCategoryInput').value;
    const contactName = document.getElementById('contactNameInput').value.trim();
    const contactEmail = document.getElementById('contactEmailInput').value.trim();
    const preferredSlot = document.getElementById('preferredSlotInput').value;
    const contactPhone = document.getElementById('contactPhoneInput').value.trim();
    const specialNotes = document.getElementById('specialNotesInput').value.trim();

    if (!brandName || !contactEmail || !contactName) {
      showToast('Please fill in all required fields', 'error');
      return;
    }

    // Generate unique confirmation reference ID
    const randomHex = Math.floor(1000 + Math.random() * 9000);
    const bookingRef = `#FEST-PITCH-2026-${randomHex}`;

    const shortlistedFests = state.shortlist.map(id => FESTS_DATA.find(f => f.id === id)).filter(Boolean);
    const totalReach = shortlistedFests.reduce((sum, f) => sum + f.footfall, 0);
    const totalBudget = shortlistedFests.reduce((sum, f) => sum + f.startingPackage, 0);

    state.lastBooking = {
      bookingRef,
      brandName,
      brandCategory,
      contactName,
      contactEmail,
      contactPhone,
      preferredSlot,
      specialNotes,
      fests: shortlistedFests.map(f => ({ id: f.id, name: f.name, college: f.college, city: f.city, package: f.startingPackage, footfall: f.footfall })),
      totalReach,
      totalBudget,
      timestamp: new Date().toISOString()
    };

    // Transition to Confirmation View
    document.getElementById('pitchFormContainer').classList.add('hidden');
    const successContainer = document.getElementById('pitchSuccessContainer');
    successContainer.classList.remove('hidden');

    document.getElementById('confirmedBookingRef').textContent = bookingRef;
    document.getElementById('confirmedBrandName').textContent = brandName;
    document.getElementById('confirmedSlot').textContent = preferredSlot;
    document.getElementById('confirmedEmail').textContent = contactEmail;
    document.getElementById('confirmedReach').textContent = `${formatNumber(totalReach)} Students`;

    showToast('Pitch call request submitted successfully!', 'success');
    refreshIcons();
  };

  window.resetPitchModalToExplore = function () {
    closePitchModal();
    // Reset form fields
    const form = document.getElementById('pitchBookingForm');
    if (form) form.reset();
  };

  // --- DOWNLOAD SHORTLIST BRIEF ---
  window.downloadShortlistSummary = function () {
    if (!state.lastBooking && state.shortlist.length === 0) {
      showToast('No active shortlist to download', 'warning');
      return;
    }

    const booking = state.lastBooking || {
      bookingRef: `#PREVIEW-${Date.now().toString().slice(-4)}`,
      brandName: 'Emerging F&B Brand',
      contactEmail: 'marketing@brand.in',
      preferredSlot: 'TBD',
      fests: state.shortlist.map(id => FESTS_DATA.find(f => f.id === id)).filter(Boolean),
      totalReach: state.shortlist.map(id => FESTS_DATA.find(f => f.id === id)).filter(Boolean).reduce((s, f) => s + f.footfall, 0),
      totalBudget: state.shortlist.map(id => FESTS_DATA.find(f => f.id === id)).filter(Boolean).reduce((s, f) => s + f.startingPackage, 0),
      timestamp: new Date().toISOString()
    };

    let summaryText = `=================================================================\n`;
    summaryText += `FESTMATCH F&B - CAMPUS SPONSORSHIP & SAMPLING CAMPAIGN BRIEF\n`;
    summaryText += `=================================================================\n\n`;
    summaryText += `Reference ID:    ${booking.bookingRef}\n`;
    summaryText += `Brand Name:      ${booking.brandName}\n`;
    summaryText += `Contact Email:   ${booking.contactEmail}\n`;
    summaryText += `Preferred Slot:  ${booking.preferredSlot}\n`;
    summaryText += `Created At:      ${booking.timestamp}\n\n`;
    summaryText += `CAMPAIGN TOTALS:\n`;
    summaryText += `-----------------------------------------------------------------\n`;
    summaryText += `Combined Reach:  ${formatNumber(booking.totalReach)} Verified Students\n`;
    summaryText += `Total Budget:    ${formatINR(booking.totalBudget)}\n`;
    summaryText += `Blended CPM:     ₹${(Math.round((booking.totalBudget / booking.totalReach) * 1000)).toLocaleString('en-IN')} / 1k students\n\n`;
    summaryText += `SHORTLISTED COLLEGE FESTIVALS:\n`;
    summaryText += `-----------------------------------------------------------------\n`;
    
    booking.fests.forEach((fest, idx) => {
      const cpm = calculateCPM(fest.startingPackage || fest.package, fest.footfall);
      summaryText += `${idx + 1}. ${fest.name} - ${fest.college} (${fest.city})\n`;
      summaryText += `   Verified Footfall: ${formatNumber(fest.footfall)} Students\n`;
      summaryText += `   Starting Package:  ${formatINR(fest.startingPackage || fest.package)}\n`;
      summaryText += `   CPM (Cost/1k):     ₹${cpm.toLocaleString('en-IN')}\n\n`;
    });

    summaryText += `=================================================================\n`;
    summaryText += `Generated via FestMatch F&B Engine\n`;

    const blob = new Blob([summaryText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `FestMatch_Campaign_Brief_${booking.bookingRef.replace('#', '')}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    showToast('Campaign brief downloaded', 'success');
  };

  // --- ABOUT MODAL ---
  window.openAboutModal = function () {
    const modal = document.getElementById('aboutModal');
    if (modal) modal.classList.remove('hidden');
    refreshIcons();
  };

  window.closeAboutModal = function () {
    const modal = document.getElementById('aboutModal');
    if (modal) modal.classList.add('hidden');
  };

  // --- TOAST NOTIFICATIONS ---
  function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `pointer-events-auto flex items-center gap-2 px-4 py-2.5 rounded-xl shadow-lg border text-xs font-semibold transition-all transform duration-200 translate-y-2 opacity-0 ${
      type === 'success'
        ? 'bg-slate-900 text-white border-emerald-500/50'
        : type === 'warning'
        ? 'bg-amber-900 text-amber-50 border-amber-600'
        : type === 'error'
        ? 'bg-rose-900 text-white border-rose-500'
        : 'bg-slate-900 text-slate-100 border-slate-700'
    }`;

    let iconHtml = '<i data-lucide="info" class="w-4 h-4 text-sky-400 shrink-0"></i>';
    if (type === 'success') {
      iconHtml = '<i data-lucide="check-circle" class="w-4 h-4 text-emerald-400 shrink-0"></i>';
    } else if (type === 'warning') {
      iconHtml = '<i data-lucide="alert-triangle" class="w-4 h-4 text-amber-400 shrink-0"></i>';
    } else if (type === 'error') {
      iconHtml = '<i data-lucide="alert-circle" class="w-4 h-4 text-rose-400 shrink-0"></i>';
    }

    toast.innerHTML = `${iconHtml}<span>${message}</span>`;
    container.appendChild(toast);
    refreshIcons();

    // Trigger enter animation
    requestAnimationFrame(() => {
      toast.classList.remove('translate-y-2', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');
    });

    // Auto-remove after 3.2s
    setTimeout(() => {
      toast.classList.remove('opacity-100');
      toast.classList.add('opacity-0', 'translate-y-2');
      setTimeout(() => {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 200);
    }, 3200);
  }

  window.toggleShortlistDrawer = function (open) {
    if (state.shortlist.length === 0) {
      showToast('Your shortlist is empty. Add up to 3 fests using the "+ Shortlist" button on any card.', 'info');
      return;
    }
    openComparisonModal();
  };

})();
