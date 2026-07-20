(() => {
  const promotionEnd = new Date('2026-08-10T10:00:00-03:00').getTime();
  const paymentUrl = 'https://campus.portalpericial.com.ar/'; // Reemplazar por el enlace real de Mercado Pago
  const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname);
  const apiBaseUrl = isLocal ? 'http://127.0.0.1:5000/api' : '/api';

  document.querySelectorAll('[data-payment-link]').forEach(a => a.href = paymentUrl);

  const el = id => document.getElementById(id);
  const tick = () => {
    const remaining = promotionEnd - Date.now();
    if (remaining <= 0) {
      ['days','hours','minutes','seconds'].forEach(id => { const node = el(id); if (node) node.textContent = '00'; });
      if (el('countdown-label')) el('countdown-label').textContent = 'LA PROMOCIÓN HA FINALIZADO';
      if (el('current-price')) el('current-price').textContent = '$150.000';
      if (el('final-price')) el('final-price').textContent = '$150.000';
      if (el('offer-note')) el('offer-note').textContent = 'Valor vigente del curso: $150.000';
      const floating = document.querySelector('.floating-cta');
      if (floating) floating.textContent = 'INSCRIBIRME · $150.000';
      return;
    }
    const d = Math.floor(remaining / 86400000);
    const h = Math.floor((remaining % 86400000) / 3600000);
    const m = Math.floor((remaining % 3600000) / 60000);
    const s = Math.floor((remaining % 60000) / 1000);
    if (el('days')) el('days').textContent = String(d).padStart(2,'0');
    if (el('hours')) el('hours').textContent = String(h).padStart(2,'0');
    if (el('minutes')) el('minutes').textContent = String(m).padStart(2,'0');
    if (el('seconds')) el('seconds').textContent = String(s).padStart(2,'0');
  };
  tick();
  setInterval(tick, 1000);

  const modal = el('reservation-modal');
  const selectedEvent = el('selected-event');
  const eventInput = el('event-input');
  const eventList = el('event-list');
  const reservationForm = el('reservation-form');
  const reservationStatus = el('reservation-status');
  const duplicateRegistration = el('duplicate-registration');
  const resendEmailButton = el('resend-email-button');
  const resendStatus = el('resend-status');
  const contactForm = el('contact-form');
  const contactStatus = el('contact-status');
  let duplicateRequest = null;

  const getDateParts = isoDate => {
    const parts = new Intl.DateTimeFormat('es-AR', {
      timeZone: 'America/Argentina/Buenos_Aires',
      weekday: 'long',
      day: '2-digit',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    }).formatToParts(new Date(isoDate));

    const value = type => parts.find(part => part.type === type)?.value ?? '';

    return {
      weekday: value('weekday'),
      day: value('day'),
      month: value('month'),
      year: value('year'),
      time: `${value('hour')}:${value('minute')}`
    };
  };

  const appendTextElement = (parent, tag, text, className = '') => {
    const element = document.createElement(tag);
    element.textContent = text;
    if (className) element.className = className;
    parent.appendChild(element);
    return element;
  };

  const openModal = (event, date) => {
    if (!modal || !selectedEvent || !eventInput) return;
    selectedEvent.textContent = `${event.titulo} · ${date.time} hs`;
    eventInput.value = String(event.eventoid);
    if (reservationStatus) {
      reservationStatus.hidden = true;
      reservationStatus.textContent = '';
    }
    if (reservationForm) {
      reservationForm.hidden = false;
      reservationForm.style.display = '';
      const button = reservationForm.querySelector('button[type="submit"]');
      if (button) {
        button.disabled = false;
        button.textContent = 'CONFIRMAR INSCRIPCIÓN';
      }
    }
    if (duplicateRegistration) duplicateRegistration.hidden = true;
    if (resendStatus) {
      resendStatus.hidden = true;
      resendStatus.textContent = '';
    }
    if (resendEmailButton) {
      resendEmailButton.disabled = false;
      resendEmailButton.textContent = 'REENVIAR CORREO';
    }
    duplicateRequest = null;
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
    setTimeout(() => modal.querySelector('input[name="nombre"]')?.focus(), 50);
  };

  const closeModal = () => {
    if (!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-open');
  };

  const createEventCard = event => {
    const date = getDateParts(event.fechainicio);
    const article = document.createElement('article');
    article.className = 'date-card';

    const calendar = document.createElement('div');
    calendar.className = 'calendar-block';
    appendTextElement(calendar, 'small', date.month.slice(0, 3).toUpperCase());
    appendTextElement(calendar, 'strong', date.day);
    appendTextElement(calendar, 'span', date.year);

    const information = document.createElement('div');
    information.className = 'date-info';
    appendTextElement(information, 'span', date.weekday.toUpperCase(), 'day-label');
    appendTextElement(information, 'h3', event.titulo);
    appendTextElement(information, 'p', event.descripcion || 'Charla informativa de Portal Pericial.');

    const metadata = document.createElement('div');
    metadata.className = 'date-meta';
    appendTextElement(metadata, 'span', `${date.time} hs`);
    appendTextElement(metadata, 'span', 'Online por Zoom');

    const button = appendTextElement(information, 'button', 'RESERVAR MI LUGAR', 'reserve-btn');
    button.type = 'button';
    button.addEventListener('click', () => openModal(event, date));

    information.insertBefore(metadata, button);
    article.append(calendar, information);

    return article;
  };

  const loadEvents = async () => {
    if (!eventList) return;

    eventList.textContent = 'Cargando próximas fechas...';

    try {
      const response = await fetch(`${apiBaseUrl}/eventos`, {
        headers: { 'Accept': 'application/json' }
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'No pudimos cargar las fechas.');
      }

      eventList.replaceChildren();

      if (data.length === 0) {
        eventList.textContent = 'Próximamente publicaremos nuevas fechas.';
        return;
      }

      data.forEach(event => eventList.appendChild(createEventCard(event)));
    } catch (error) {
      eventList.textContent = error.message || 'No pudimos cargar las fechas en este momento.';
    }
  };

  const submitJson = async (url, payload) => {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    let data;
    try {
      data = await response.json();
    } catch {
      data = {};
    }

    if (!response.ok) {
      throw new Error(data.error || 'No pudimos completar el envío. Intentá nuevamente.');
    }

    return data;
  };

  reservationForm?.addEventListener('submit', async event => {
    event.preventDefault();

    const data = new FormData(reservationForm);
    const button = reservationForm.querySelector('button[type="submit"]');
    const originalText = button.textContent;

    if (reservationStatus) {
      reservationStatus.hidden = true;
      reservationStatus.textContent = '';
    }

    button.disabled = true;
    button.textContent = 'ENVIANDO...';

    try {
      const payload = {
        nombre: data.get('nombre'),
        apellido: data.get('apellido'),
        email: data.get('email'),
        whatsapp: data.get('whatsapp'),
        eventoid: Number(data.get('eventoid')),
        _honey: data.get('_honey')
      };
      const result = await submitJson(`${apiBaseUrl}/inscripciones`, payload);

      if (result.inscripcioncreada === false) {
        duplicateRequest = {
          email: payload.email,
          eventoid: payload.eventoid,
          _honey: payload._honey
        };
        button.disabled = false;
        button.textContent = originalText;
        reservationForm.hidden = true;
        reservationForm.style.display = 'none';
        if (duplicateRegistration) duplicateRegistration.hidden = false;
        resendEmailButton?.focus();
        return;
      }

      const eventDescription = selectedEvent?.textContent || '';
      window.location.href = `gracias.html?tipo=charla&evento=${encodeURIComponent(eventDescription)}`;
    } catch (error) {
      if (reservationStatus) {
        reservationStatus.textContent = error.message;
        reservationStatus.hidden = false;
      }
      button.disabled = false;
      button.textContent = originalText;
    }
  });

  resendEmailButton?.addEventListener('click', async () => {
    if (!duplicateRequest) return;

    const originalText = resendEmailButton.textContent;

    if (resendStatus) {
      resendStatus.hidden = true;
      resendStatus.textContent = '';
    }

    resendEmailButton.disabled = true;
    resendEmailButton.textContent = 'REENVIANDO...';

    try {
      const result = await submitJson(
        `${apiBaseUrl}/inscripciones/reenviar-correo`,
        duplicateRequest
      );

      if (resendStatus) {
        resendStatus.textContent = result.mensaje;
        resendStatus.hidden = false;
      }
      resendEmailButton.textContent = 'CORREO REENVIADO';
    } catch (error) {
      if (resendStatus) {
        resendStatus.textContent = error.message;
        resendStatus.hidden = false;
      }
      resendEmailButton.disabled = false;
      resendEmailButton.textContent = originalText;
    }
  });

  contactForm?.addEventListener('submit', async event => {
    event.preventDefault();

    const data = new FormData(contactForm);
    const button = contactForm.querySelector('button[type="submit"]');
    const originalText = button.textContent;

    if (contactStatus) {
      contactStatus.hidden = true;
      contactStatus.textContent = '';
    }

    button.disabled = true;
    button.textContent = 'ENVIANDO...';

    try {
      await submitJson(`${apiBaseUrl}/consultas`, {
        nombrecompleto: data.get('nombrecompleto'),
        email: data.get('email'),
        whatsapp: data.get('whatsapp'),
        consulta: data.get('consulta'),
        _honey: data.get('_honey')
      });

      window.location.href = 'gracias.html?tipo=consulta';
    } catch (error) {
      if (contactStatus) {
        contactStatus.textContent = error.message;
        contactStatus.hidden = false;
      }
      button.disabled = false;
      button.textContent = originalText;
    }
  });

  document.querySelectorAll('[data-close-modal]').forEach(button => button.addEventListener('click', closeModal));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && modal && modal.classList.contains('open')) {
      closeModal();
    }
  });

  loadEvents();
})();
