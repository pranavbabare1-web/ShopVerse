/* ── ShopVerse Main JS ─────────────────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {

  // ── Navbar scroll effect ──────────────────────────────────────────────────
  const navbar = document.getElementById('mainNav');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) navbar?.classList.add('scrolled');
    else navbar?.classList.remove('scrolled');
  }, { passive: true });

  // ── Hamburger / Mobile menu ───────────────────────────────────────────────
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');
  hamburger?.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    mobileMenu?.classList.toggle('open');
  });

  // Close mobile menu on outside click
  document.addEventListener('click', (e) => {
    if (mobileMenu?.classList.contains('open') &&
        !mobileMenu.contains(e.target) &&
        !hamburger?.contains(e.target)) {
      mobileMenu.classList.remove('open');
      hamburger?.classList.remove('open');
    }
  });

  // ── Auto-dismiss messages ─────────────────────────────────────────────────
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s, transform 0.5s';
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(100%)';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });

  // ── Add-to-cart AJAX (product list quick-add) ─────────────────────────────
  document.querySelectorAll('.product-card form').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      const original = btn.innerHTML;
      btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
      btn.disabled = true;

      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await res.json();

        if (data.success) {
          btn.innerHTML = '<i class="fas fa-check"></i>';
          btn.style.background = '#10b981';
          updateCartBadge(data.cart_count);
          showToast(data.message, 'success');
          setTimeout(() => {
            btn.innerHTML = original;
            btn.style.background = '';
            btn.disabled = false;
          }, 1500);
        }
      } catch {
        btn.innerHTML = original;
        btn.disabled = false;
      }
    });
  });

  // ── Cart badge live update ────────────────────────────────────────────────
  function updateCartBadge(count) {
    const badges = document.querySelectorAll('.cart-badge');
    const cartBtns = document.querySelectorAll('.cart-btn');
    if (count > 0) {
      if (badges.length > 0) {
        badges.forEach(b => { b.textContent = count; });
      } else {
        cartBtns.forEach(btn => {
          const badge = document.createElement('span');
          badge.className = 'cart-badge';
          badge.textContent = count;
          btn.appendChild(badge);
        });
      }
    }
  }

  // ── Toast notification ────────────────────────────────────────────────────
  function showToast(message, type = 'success') {
    const container = document.getElementById('messagesContainer') || createToastContainer();
    const toast = document.createElement('div');
    const icon = type === 'success' ? 'fa-circle-check' : type === 'error' ? 'fa-circle-xmark' : 'fa-circle-info';
    toast.className = `alert alert-${type}`;
    toast.innerHTML = `<i class="fas ${icon}"></i> ${message} <button class="alert-close" onclick="this.parentElement.remove()">×</button>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.transition = 'opacity 0.5s, transform 0.5s';
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 500);
    }, 3500);
  }

  function createToastContainer() {
    const c = document.createElement('div');
    c.className = 'messages-container';
    c.id = 'messagesContainer';
    document.body.appendChild(c);
    return c;
  }

  // ── Smooth scroll for anchor links ───────────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Newsletter form ───────────────────────────────────────────────────────
  const newsletterForm = document.querySelector('.newsletter-form');
  newsletterForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const input = newsletterForm.querySelector('input');
    if (input?.value) {
      showToast('Thanks for subscribing! 🎉', 'success');
      input.value = '';
    }
  });
  // Allow button click in newsletter
  const subBtn = document.querySelector('.btn-subscribe');
  subBtn?.addEventListener('click', () => {
    const input = document.querySelector('.newsletter-form input');
    if (input?.value) {
      showToast('Thanks for subscribing! 🎉', 'success');
      input.value = '';
    } else {
      showToast('Please enter your email address.', 'info');
    }
  });

  // ── Image lazy load fallback ──────────────────────────────────────────────
  document.querySelectorAll('img[loading="lazy"]').forEach(img => {
    img.addEventListener('error', function () {
      this.style.display = 'none';
      const placeholder = document.createElement('div');
      placeholder.className = 'no-image-placeholder';
      placeholder.innerHTML = '<i class="fas fa-image fa-2x"></i>';
      this.parentNode.insertBefore(placeholder, this);
    });
  });

  // ── Product detail qty input validation ──────────────────────────────────
  const qtyInput = document.getElementById('qtyInput');
  qtyInput?.addEventListener('input', function () {
    const max = parseInt(this.max) || 999;
    let val = parseInt(this.value) || 1;
    if (val < 1) val = 1;
    if (val > max) val = max;
    this.value = val;
  });

  // ── Sticky summary active scroll ──────────────────────────────────────────
  // (Handled via CSS position:sticky — nothing needed here)

  // ── Form validation UX ────────────────────────────────────────────────────
  document.querySelectorAll('.form-control').forEach(input => {
    input.addEventListener('blur', function () {
      if (this.required && !this.value.trim()) {
        this.style.borderColor = 'var(--danger)';
      } else {
        this.style.borderColor = '';
      }
    });
    input.addEventListener('input', function () {
      this.style.borderColor = '';
    });
  });

  // ── Back to top button ────────────────────────────────────────────────────
  const backToTop = document.createElement('button');
  backToTop.innerHTML = '<i class="fas fa-chevron-up"></i>';
  backToTop.className = 'back-to-top';
  backToTop.setAttribute('aria-label', 'Back to top');
  backToTop.style.cssText = `
    position: fixed; bottom: 28px; right: 28px;
    width: 44px; height: 44px; border-radius: 50%;
    background: var(--primary); color: #fff; border: none;
    cursor: pointer; font-size: 1rem; opacity: 0; visibility: hidden;
    transition: all 0.3s; z-index: 900; box-shadow: 0 4px 16px rgba(108,71,255,.4);
  `;
  document.body.appendChild(backToTop);
  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      backToTop.style.opacity = '1';
      backToTop.style.visibility = 'visible';
    } else {
      backToTop.style.opacity = '0';
      backToTop.style.visibility = 'hidden';
    }
  }, { passive: true });
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

});
