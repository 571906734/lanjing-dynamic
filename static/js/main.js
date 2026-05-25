/**
 * LanJing Ship Service - Main JavaScript
 * No external dependencies
 */

document.addEventListener('DOMContentLoaded', function () {

  // ==========================================================================
  // 1. MOBILE HAMBURGER MENU
  // ==========================================================================
  const hamburger = document.querySelector('.hamburger');
  const mainNav = document.querySelector('.main-nav');
  const dropdowns = document.querySelectorAll('.dropdown');

  if (hamburger && mainNav) {
    hamburger.addEventListener('click', function () {
      mainNav.classList.toggle('open');
    });
  }

  // Mobile dropdown toggle
  dropdowns.forEach(function (dd) {
    const toggle = dd.querySelector('.dropdown-toggle');
    if (toggle) {
      toggle.addEventListener('click', function (e) {
        if (window.innerWidth <= 768) {
          e.preventDefault();
          dd.classList.toggle('open');
        }
      });
    }
  });

  // Close menu on link click (mobile)
  mainNav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      if (window.innerWidth <= 768) {
        mainNav.classList.remove('open');
        dropdowns.forEach(function (d) { d.classList.remove('open'); });
      }
    });
  });

  // ==========================================================================
  // 2. HERO BANNER AUTOPLAY
  // ==========================================================================
  const slides = document.querySelectorAll('.hero-slide');
  const indicators = document.querySelectorAll('.hero-indicator');
  let currentSlide = 0;
  const totalSlides = slides.length;
  let slideInterval;

  function goToSlide(index) {
    slides.forEach(function (s) { s.classList.remove('active'); });
    indicators.forEach(function (i) { i.classList.remove('active'); });
    slides[index].classList.add('active');
    indicators[index].classList.add('active');
    currentSlide = index;
  }

  function nextSlide() {
    goToSlide((currentSlide + 1) % totalSlides);
  }

  if (totalSlides > 1) {
    slideInterval = setInterval(nextSlide, 5000);
    indicators.forEach(function (ind, idx) {
      ind.addEventListener('click', function () {
        clearInterval(slideInterval);
        goToSlide(idx);
        slideInterval = setInterval(nextSlide, 5000);
      });
    });
  }

  // ==========================================================================
  // 3. NUMBER COUNT-UP ANIMATION (Scroll Trigger)
  // ==========================================================================
  const statNumbers = document.querySelectorAll('.stat-number');
  let statsAnimated = false;

  function animateNumbers() {
    if (statsAnimated) return;
    const statsSection = document.querySelector('.stats-section');
    if (!statsSection) return;

    const rect = statsSection.getBoundingClientRect();
    if (rect.top < window.innerHeight - 100 && rect.bottom > 0) {
      statsAnimated = true;
      statNumbers.forEach(function (el) {
        const target = parseInt(el.getAttribute('data-target'), 10);
        const duration = 1800;
        const startTime = performance.now();

        function update(now) {
          const elapsed = now - startTime;
          const progress = Math.min(elapsed / duration, 1);
          // Ease-out
          const eased = 1 - Math.pow(1 - progress, 3);
          const current = Math.floor(eased * target);
          el.textContent = current;
          if (progress < 1) {
            requestAnimationFrame(update);
          } else {
            el.textContent = target;
          }
        }
        requestAnimationFrame(update);
      });
    }
  }

  window.addEventListener('scroll', animateNumbers);
  animateNumbers(); // check on load

  // ==========================================================================
  // 4. SMOOTH SCROLL ANCHOR
  // ==========================================================================
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var targetId = this.getAttribute('href').substring(1);
      var target = document.getElementById(targetId);
      if (target) {
        e.preventDefault();
        var offset = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--header-height'), 10) || 72;
        var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });

  // ==========================================================================
  // 5. FORM VALIDATION
  // ==========================================================================
  var forms = document.querySelectorAll('form');
  forms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      var valid = true;
      var requiredFields = form.querySelectorAll('[required]');

      requiredFields.forEach(function (field) {
        var group = field.closest('.form-group');
        if (!group) return;

        group.classList.remove('error');

        if (field.type === 'email') {
          var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!field.value.trim() || !emailRe.test(field.value.trim())) {
            group.classList.add('error');
            valid = false;
          }
        } else if (field.tagName === 'SELECT') {
          if (!field.value || field.value === '') {
            group.classList.add('error');
            valid = false;
          }
        } else if (field.type === 'checkbox') {
          if (!field.checked) {
            group.classList.add('error');
            valid = false;
          }
        } else {
          if (!field.value.trim()) {
            group.classList.add('error');
            valid = false;
          }
        }
      });

      if (!valid) {
        e.preventDefault();
        // Scroll to first error
        var firstError = form.querySelector('.form-group.error');
        if (firstError) {
          firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      } else {
        // Only intercept the quote request form; let other forms (login, register, etc.) submit normally
        var action = (form.getAttribute('action') || '').toLowerCase();
        if (action.indexOf('quote') !== -1 || action.indexOf('contact') !== -1) {
          e.preventDefault();
          var submitBtn = form.querySelector('button[type="submit"]');
          var originalText = submitBtn ? submitBtn.textContent : '';
          if (submitBtn) {
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
          }
          setTimeout(function () {
            if (submitBtn) {
              submitBtn.textContent = 'Quote Request Sent!';
              submitBtn.style.background = '#27ae60';
              submitBtn.style.borderColor = '#27ae60';
            }
            form.reset();
            setTimeout(function () {
              if (submitBtn) {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                submitBtn.style.background = '';
                submitBtn.style.borderColor = '';
              }
            }, 3000);
          }, 1500);
        }
        // Other forms (login, register, etc.) will submit normally — no preventDefault called.
      }
    });

    // Real-time validation clear
    form.querySelectorAll('input, select, textarea').forEach(function (field) {
      field.addEventListener('input', function () {
        var group = field.closest('.form-group');
        if (group && group.classList.contains('error')) {
          if (field.value.trim()) {
            if (field.type === 'email') {
              var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
              if (re.test(field.value.trim())) {
                group.classList.remove('error');
              }
            } else {
              group.classList.remove('error');
            }
          }
        }
      });
      field.addEventListener('change', function () {
        var group = field.closest('.form-group');
        if (group && group.classList.contains('error') && field.value) {
          group.classList.remove('error');
        }
      });
    });
  });

  // ==========================================================================
  // 6. CASE STUDY FILTER
  // ==========================================================================
  var filterTabs = document.querySelectorAll('.filter-tab');
  var caseCards = document.querySelectorAll('.case-card');

  filterTabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      filterTabs.forEach(function (t) { t.classList.remove('active'); });
      tab.classList.add('active');
      var filter = tab.getAttribute('data-filter');

      caseCards.forEach(function (card) {
        if (filter === 'all' || card.getAttribute('data-category') === filter) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });

  // ==========================================================================
  // 7. ACCORDION (Supply & Technical pages)
  // ==========================================================================
  var accordionItems = document.querySelectorAll('.accordion-item');
  accordionItems.forEach(function (item) {
    var header = item.querySelector('.accordion-header');
    if (!header) return;
    header.addEventListener('click', function () {
      var isActive = item.classList.contains('active');
      // Close all
      accordionItems.forEach(function (ai) { ai.classList.remove('active'); });
      // Open clicked if not already active
      if (!isActive) {
        item.classList.add('active');
      }
    });
  });

  // ==========================================================================
  // 8. HEADER SHADOW ON SCROLL
  // ==========================================================================
  var header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', function () {
      if (window.pageYOffset > 10) {
        header.style.boxShadow = '0 2px 12px rgba(0,0,0,0.12)';
      } else {
        header.style.boxShadow = '';
      }
    });
  }

  // ==========================================================================
  // 9. ACTIVE NAV LINK HIGHLIGHT
  // ==========================================================================
  var currentPath = window.location.pathname;
  var navLinks = document.querySelectorAll('.main-nav a');
  navLinks.forEach(function (link) {
    var href = link.getAttribute('href');
    if (href && currentPath.endsWith(href)) {
      link.classList.add('active');
    }
  });
  // Homepage default
  if (currentPath.endsWith('/') || currentPath.endsWith('index.html')) {
    var homeLink = document.querySelector('.main-nav a[href="index.html"]');
    if (homeLink) homeLink.classList.add('active');
  }
});