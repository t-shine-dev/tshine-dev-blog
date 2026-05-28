/* ============================================================
   TSHINE DEV BLOG ⭐ — main.js
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {

    /* --- Page Loader --- */
    const loader = document.getElementById('page-loader');
    if (loader) {
        const hide = () => loader.classList.add('hidden');
        if (document.readyState === 'complete') { setTimeout(hide, 300); }
        else { window.addEventListener('load', () => setTimeout(hide, 300)); }
        setTimeout(hide, 1800);
    }

    /* --- Theme --- */
    const themeBtn  = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const html      = document.documentElement;
    const applyTheme = (t) => {
        html.setAttribute('data-theme', t);
        if (themeIcon) themeIcon.className = t === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
    };
    applyTheme(localStorage.getItem('theme') || 'light');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            localStorage.setItem('theme', next);
            applyTheme(next);
        });
    }

    /* --- Navbar shadow on scroll --- */
    const navbar = document.querySelector('.site-navbar');
    if (navbar) window.addEventListener('scroll', () => navbar.classList.toggle('scrolled', window.scrollY > 20), { passive: true });

    /* --- Reading progress --- */
    const bar = document.getElementById('reading-progress');
    if (bar) {
        window.addEventListener('scroll', () => {
            const body = document.querySelector('.post-body');
            if (!body) return;
            const rect = body.getBoundingClientRect();
            const pct  = Math.min(100, Math.max(0, -rect.top / (rect.height - window.innerHeight) * 100));
            bar.style.width = pct + '%';
        }, { passive: true });
    }

    /* --- Back to top --- */
    const btt = document.getElementById('back-to-top');
    if (btt) {
        window.addEventListener('scroll', () => btt.classList.toggle('visible', window.scrollY > 400), { passive: true });
        btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    /* --- Scroll-in animations for post cards --- */
    const cardObs = new IntersectionObserver((entries) => {
        entries.forEach((e, i) => {
            if (e.isIntersecting) {
                const delay = Number(e.target.dataset.delay || 0);
                setTimeout(() => e.target.classList.add('visible'), delay);
                cardObs.unobserve(e.target);
            }
        });
    }, { threshold: 0.07, rootMargin: '0px 0px -20px 0px' });

    document.querySelectorAll('.post-card').forEach((el, i) => {
        el.dataset.delay = (i % 3) * 75;
        cardObs.observe(el);
    });

    /* --- Generic fade-in for other elements --- */
    const fadeObs = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.style.opacity  = '1';
                e.target.style.transform = 'translateY(0)';
                fadeObs.unobserve(e.target);
            }
        });
    }, { threshold: 0.09 });

    document.querySelectorAll('.category-chip, .stat-card, .dash-card').forEach(el => {
        Object.assign(el.style, {
            opacity: '0', transform: 'translateY(16px)',
            transition: 'opacity 0.45s cubic-bezier(0.22,1,0.36,1), transform 0.45s cubic-bezier(0.22,1,0.36,1)'
        });
        fadeObs.observe(el);
    });

    /* --- Animated counters --- */
    document.querySelectorAll('.stat-num[data-target]').forEach(el => {
        const target = parseInt(el.dataset.target, 10);
        const cntObs = new IntersectionObserver(([entry]) => {
            if (!entry.isIntersecting) return;
            cntObs.unobserve(el);
            const start = performance.now();
            const step  = (now) => {
                const t = Math.min((now - start) / 1200, 1);
                el.textContent = Math.round((1 - Math.pow(1 - t, 3)) * target).toLocaleString();
                if (t < 1) requestAnimationFrame(step);
            };
            requestAnimationFrame(step);
        }, { threshold: 0.5 });
        cntObs.observe(el);
    });

    /* --- Toast helper --- */
    window.showToast = (msg, duration = 3200) => {
        let tray = document.querySelector('.toast-tray');
        if (!tray) { tray = Object.assign(document.createElement('div'), { className: 'toast-tray' }); document.body.appendChild(tray); }
        const t = Object.assign(document.createElement('div'), { className: 'toast-pop', textContent: msg });
        tray.appendChild(t);
        setTimeout(() => {
            Object.assign(t.style, { transition: 'opacity 0.3s, transform 0.3s', opacity: '0', transform: 'translateX(40px)' });
            setTimeout(() => t.remove(), 320);
        }, duration);
    };

    /* --- AJAX Bookmarks --- */
    document.querySelectorAll('.bm-btn, .bm-btn-lg').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const href = btn.getAttribute('href');
            if (!href) return;
            e.preventDefault();
            try {
                const res  = await fetch(href, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
                const data = await res.json();
                btn.classList.toggle('bookmarked', data.bookmarked);
                const icon = btn.querySelector('i');
                if (icon) icon.className = data.bookmarked ? 'bi bi-bookmark-fill' : 'bi bi-bookmark';
                const txt = [...btn.childNodes].find(n => n.nodeType === Node.TEXT_NODE);
                if (txt) txt.textContent = data.bookmarked ? ' Saved' : ' Save';
                showToast(data.bookmarked ? '⭐ Saved to bookmarks' : 'Removed from bookmarks');
            } catch { window.location.href = href; }
        });
    });

    /* --- Ripple on buttons --- */
    document.querySelectorAll('.btn-primary-brand, .btn-auth, .btn-primary').forEach(btn => {
        btn.style.overflow = 'hidden';
        btn.addEventListener('click', (e) => {
            const rect = btn.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const r = document.createElement('span');
            Object.assign(r.style, {
                position: 'absolute', borderRadius: '50%', background: 'rgba(255,255,255,0.3)',
                width: `${size}px`, height: `${size}px`,
                left: `${e.clientX - rect.left - size / 2}px`,
                top:  `${e.clientY - rect.top  - size / 2}px`,
                transform: 'scale(0)', animation: 'ripple 0.55s linear', pointerEvents: 'none'
            });
            btn.appendChild(r);
            setTimeout(() => r.remove(), 560);
        });
    });

    /* --- Image fade-in --- */
    document.querySelectorAll('.card-img, .detail-cover').forEach(img => {
        img.style.cssText += 'opacity:0;transition:opacity 0.4s ease;';
        if (img.complete) img.style.opacity = '1';
        else img.addEventListener('load', () => img.style.opacity = '1');
    });
});

/* Inject ripple keyframe once */
if (!document.getElementById('_ripple_kf')) {
    const s = Object.assign(document.createElement('style'), {
        id: '_ripple_kf',
        textContent: '@keyframes ripple { to { transform: scale(2.8); opacity: 0; } }'
    });
    document.head.appendChild(s);
}
