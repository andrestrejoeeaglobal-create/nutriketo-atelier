
    document.addEventListener('DOMContentLoaded', () => {
      try {
        if ('serviceWorker' in navigator) {
          navigator.serviceWorker.register('./sw.js?v=nutriketo-v36-6-rev3-s40-ui-align-v13')
            .then((reg) => console.log('[ServiceWorker] Registrado exitosamente en alcance:', reg.scope))
            .catch((err) => console.error('[ServiceWorker] Error en registro:', err));
        }
        if (typeof loadAppState === 'function') loadAppState();
        const overlay = document.getElementById('setup-overlay');
        const mainContent = document.getElementById('main-app-content');
        if (overlay) overlay.style.display = 'none';
        if (mainContent) mainContent.style.display = 'block';

        const setupWeekSelect = document.getElementById('setup-week');
        if (setupWeekSelect && activeWeek) setupWeekSelect.value = activeWeek;

        const headerWeekSelect = document.getElementById('header-week-select');
        if (headerWeekSelect && activeWeek) headerWeekSelect.value = activeWeek;

        const headerSubtitle = document.getElementById('header-week-subtitle');
        if (headerSubtitle && activeWeek) headerSubtitle.innerText = `${activeWeek} | Ecosistema T.I.L.O.®`;

        if (typeof renderDateBar === 'function') renderDateBar();
        const initIdx = (typeof selectedIdx === 'number' && !isNaN(selectedIdx) && selectedIdx >= 0) ? selectedIdx : 0;
        if (typeof renderDay === 'function') renderDay(initIdx);
        if (typeof switchTab === 'function') switchTab('design');
      } catch (e) {
        console.error("Error en auto-init:", e);
      }
    });
  