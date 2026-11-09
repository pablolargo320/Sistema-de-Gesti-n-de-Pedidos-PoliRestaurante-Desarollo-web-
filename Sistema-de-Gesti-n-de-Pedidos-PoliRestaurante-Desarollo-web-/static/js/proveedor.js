
(() => {
    "use strict";

    const API = {
        proveedores: "/api/proveedores",
        productos: "/api/productos",
        solicitudes: "/api/solicitudes-abastecimiento",
        despachos: "/api/despachos"
    };

    const state = {
        proveedores: [],
        productos: [],
        proveedorActual: null,
        solicitudes: [],
        despachos: [],
        historial: [],
        vistaActual: "solicitudes"
    };

    const $ = (selector) => document.querySelector(selector);
    const $$ = (selector) => [...document.querySelectorAll(selector)];

    // ==========================================
    // FUNCIONES GENERALES
    // ==========================================

    async function getJSON(url, options = {}) {

        const config = {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {})
            }
        };

        const response = await fetch(url, config);
        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(
                data.error || data.mensaje || `Error HTTP ${response.status}`
            );
        }

        return data;
    }

    function notify(message, isError = false) {

        const toast = $("#toast");

        toast.textContent = message;
        toast.style.background = isError ? "#8d3d3d" : "#203850";
        toast.classList.add("show");

        window.clearTimeout(notify.timer);

        notify.timer = window.setTimeout(
            () => toast.classList.remove("show"),
            3500
        );
    }

    function escapeHTML(value) {

        return String(value ?? "").replace(/[&<>"']/g, (char) => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        })[char]);
    }

    function setConnection(online, message) {

        const text = $("#connectionText");
        const dot = document.querySelector(
            ".connection-indicator .status-dot"
        );

        text.textContent = message;
        dot.classList.toggle("online", online);

        $("#dbStatus").textContent = online
            ? "Conectada"
            : "Sin conexión";
    }

    function setFeatureStatus(id, online, message) {

        const element = $(id);

        if (!element) return;

        element.textContent = message;

        element.classList.toggle("live-state", online);
        element.classList.toggle("pending-state", !online);
    }

    function labelEstado(estado) {

        const labels = {
            pendiente: "Pendiente",
            aceptada: "Aceptada",
            rechazada: "Rechazada",
            en_despacho: "En despacho",
            completada: "Completada",
            cancelada: "Cancelada",
            preparando: "Preparando",
            despachado: "Despachado",
            en_transito: "En tránsito",
            entregado: "Entregado",
            con_novedad: "Con novedad"
        };

        return labels[estado] || estado || "Sin estado";
    }

    function badgeEstado(estado) {

        const clases = {
            pendiente: "pending",
            preparando: "pending",
            aceptada: "success",
            despachado: "info",
            en_transito: "info",
            en_despacho: "info",
            completada: "success",
            entregado: "success",
            rechazada: "danger",
            cancelada: "muted",
            con_novedad: "warning"
        };

        return `
            <span class="status-chip ${clases[estado] || "muted"}">
                ${escapeHTML(labelEstado(estado))}
            </span>
        `;
    }

    function fechaCorta(value) {

        if (!value) return "—";

        const date = new Date(value.replace(" ", "T"));

        if (Number.isNaN(date.getTime())) {
            return escapeHTML(value);
        }

        return new Intl.DateTimeFormat(
            "es-CO",
            { dateStyle: "medium" }
        ).format(date);
    }


    // ==========================================
    // NAVEGACIÓN ENTRE LAS CUATRO FUNCIONALIDADES
    // ==========================================

    function changeView(view) {

        state.vistaActual = view;

        $$(".nav-link").forEach((button) => {
            button.classList.toggle(
                "active",
                button.dataset.view === view
            );
        });

        $$(".view-panel").forEach((panel) => {
            panel.classList.toggle(
                "active",
                panel.id === `view-${view}`
            );
        });

        const labels = {
            solicitudes: [
                "Solicitudes de abastecimiento",
                "Solicitudes"
            ],
            despachos: [
                "Despachos y entregas",
                "Despachos y entregas"
            ],
            historial: [
                "Historial y perfil del proveedor",
                "Historial y perfil"
            ],
            catalogo: [
                "Catálogo de productos suministrados",
                "Catálogo suministrado"
            ]
        };

        const descriptions = {
            solicitudes:
                "Revisa las solicitudes del restaurante y gestiona su atención.",

            despachos:
                "Registra despachos y confirma la recepción de los productos.",

            historial:
                "Mantén actualizada la información comercial y consulta operaciones anteriores.",

            catalogo:
                "Consulta el producto asociado y su disponibilidad actual."
        };

        $("#pageTitle").textContent = labels[view][0];
        $("#breadcrumbCurrent").textContent = labels[view][1];
        $("#pageDescription").textContent = descriptions[view];

        $("#sidebar").classList.remove("open");
    }


    // ==========================================
    // PROVEEDORES Y PRODUCTOS
    // ==========================================

    function fillProviderSelector() {

        const select = $("#providerSelect");

        select.innerHTML = "";

        if (!state.proveedores.length) {

            select.add(
                new Option("No hay proveedores registrados", "")
            );

            select.disabled = true;

            return;
        }

        state.proveedores.forEach((provider) => {

            select.add(
                new Option(
                    `${provider.nombre} · #${provider.id_proveedor}`,
                    provider.id_proveedor
                )
            );

        });

        const requestedId = new URLSearchParams(
            window.location.search
        ).get("id_proveedor");

        const savedId = sessionStorage.getItem(
            "proveedorSeleccionado"
        );

        const chosen =
            state.proveedores.find(
                (item) => String(item.id_proveedor) === requestedId
            )
            ||
            state.proveedores.find(
                (item) => String(item.id_proveedor) === savedId
            )
            ||
            state.proveedores[0];

        select.value = String(chosen.id_proveedor);
        select.disabled = false;

        select.dispatchEvent(new Event("change"));
    }

    function fillProductOptions() {

        const select = $("#profileProduct");

        select.innerHTML = "";

        select.add(
            new Option("Sin producto asociado", "")
        );

        state.productos.forEach((product) => {

            select.add(
                new Option(
                    `${product.nombre} · #${product.id_producto}`,
                    product.id_producto
                )
            );

        });
    }

    function renderProfile() {

        const provider = state.proveedorActual;

        if (!provider) return;

        $("#profileName").value = provider.nombre || "";
        $("#profilePhone").value = provider.telefono || "";
        $("#profileEmail").value = provider.correo || "";
        $("#profileAddress").value = provider.direccion || "";

        $("#profileProduct").value =
            provider.producto_id_producto ?? "";

        $("#profileIdentifier").textContent =
            `ID ${provider.id_proveedor} · ${provider.nombre}`;

        $("#profileMessage").textContent = "";

        $("#profileMessage").classList.remove("error");
    }

    function renderCatalog() {

        const container = $("#catalogContent");
        const provider = state.proveedorActual;

        if (!provider) {

            container.innerHTML = `
                <div class="loading-card">
                    Selecciona un proveedor para consultar el catálogo.
                </div>
            `;

            $("#productCount").textContent = "0";

            return;
        }

        const product = state.productos.find(
            (item) =>
                Number(item.id_producto) ===
                Number(provider.producto_id_producto)
        );

        if (!product) {

            $("#productCount").textContent = "0";

            container.innerHTML = `
                <div class="loading-card">
                    Este proveedor no tiene un producto asociado.
                    Puedes asignarlo desde “Historial y perfil”.
                </div>
            `;

            return;
        }

        $("#productCount").textContent = "1";

        const available = Boolean(product.disponible);

        const price =
            product.precio === null ||
            product.precio === undefined
                ? "Precio no registrado"
                : new Intl.NumberFormat(
                    "es-CO",
                    {
                        style: "currency",
                        currency: "COP",
                        maximumFractionDigits: 0
                    }
                ).format(Number(product.precio));

        container.innerHTML = `
            <article class="product-card">

                <div class="product-art" aria-hidden="true">
                    ▦
                </div>

                <h3>
                    ${escapeHTML(product.nombre || "Producto")}
                </h3>

                <p>
                    ${escapeHTML(
                        product.descripcion ||
                        "Sin descripción registrada."
                    )}
                </p>

                <div class="product-meta">

                    <span class="product-price">
                        ${escapeHTML(price)}
                    </span>

                    <span class="availability ${
                        available ? "available" : "unavailable"
                    }">
                        ${available ? "Disponible" : "No disponible"}
                    </span>

                </div>

            </article>
        `;
    }


    // ==========================================
    // 1. SOLICITUDES DE ABASTECIMIENTO
    // ==========================================

    function renderSolicitudes() {

        const body = $("#requestsTableBody");

        const term = $("#requestSearch").value
            .trim()
            .toLowerCase();

        const status = $("#requestStatusFilter").value;

        const filtered = state.solicitudes.filter((item) => {

            const matchesStatus =
                !status || item.estado === status;

            const matchesTerm =
                !term
                ||
                String(item.id_solicitud).includes(term)
                ||
                String(item.producto_nombre || "")
                    .toLowerCase()
                    .includes(term);

            return matchesStatus && matchesTerm;
        });

        $("#pendingCount").textContent =
            state.solicitudes.filter(
                (item) => item.estado === "pendiente"
            ).length;

        if (!filtered.length) {

            body.innerHTML = `
                <tr>
                    <td colspan="6">

                        <div class="empty-state">

                            <span class="empty-icon">▤</span>

                            <strong>
                                No hay solicitudes para mostrar
                            </strong>

                            <p>
                                Cuando el restaurante genere solicitudes
                                para este proveedor, aparecerán aquí.
                            </p>

                        </div>

                    </td>
                </tr>
            `;

            renderDispatchRequestOptions();

            return;
        }

        body.innerHTML = filtered.map((item) => {

            const actions = item.estado === "pendiente"

                ? `
                    <div class="action-group">

                        <button
                            class="mini-button accept"
                            data-request-action="aceptada"
                            data-id="${item.id_solicitud}"
                            type="button">
                            Aceptar
                        </button>

                        <button
                            class="mini-button reject"
                            data-request-action="rechazada"
                            data-id="${item.id_solicitud}"
                            type="button">
                            Rechazar
                        </button>

                    </div>
                `

                : (
                    item.estado === "rechazada" &&
                    item.motivo_rechazo

                    ? `
                        <span
                            class="muted-text"
                            title="${escapeHTML(item.motivo_rechazo)}">
                            Ver motivo
                        </span>
                    `

                    : `
                        <span class="muted-text">
                            Sin acciones
                        </span>
                    `
                );

            return `
                <tr>

                    <td>
                        <strong>#${item.id_solicitud}</strong>

                        <small class="table-subtext">
                            ${fechaCorta(item.fecha_solicitud)}
                        </small>
                    </td>

                    <td>
                        ${escapeHTML(item.producto_nombre || "Producto")}
                    </td>

                    <td>
                        ${Number(item.cantidad_solicitada)
                            .toLocaleString("es-CO")} unidades
                    </td>

                    <td>
                        ${fechaCorta(item.fecha_requerida)}
                    </td>

                    <td>
                        ${badgeEstado(item.estado)}
                    </td>

                    <td>
                        ${actions}
                    </td>

                </tr>
            `;

        }).join("");

        renderDispatchRequestOptions();
    }


    function renderDispatchRequestOptions() {

        const select = $("#dispatchRequest");

        const previous = select.value;

        const disponibles = state.solicitudes.filter((item) =>

            ["aceptada", "en_despacho"].includes(item.estado)

            &&
            Number(item.cantidad_pendiente_despacho) > 0

        );

        select.innerHTML = "";

        select.add(
            new Option(
                disponibles.length
                    ? "Selecciona una solicitud"
                    : "No hay solicitudes aceptadas con saldo pendiente",
                ""
            )
        );

        disponibles.forEach((item) => {

            select.add(
                new Option(
                    `#${item.id_solicitud} · ${item.producto_nombre} · Pendiente: ${item.cantidad_pendiente_despacho}`,
                    item.id_solicitud
                )
            );

        });

        select.value = disponibles.some(
            (item) => String(item.id_solicitud) === previous
        )
            ? previous
            : "";

        const seleccionada = disponibles.find(
            (item) => String(item.id_solicitud) === select.value
        );

        $("#dispatchQuantity").max = seleccionada
            ? seleccionada.cantidad_pendiente_despacho
            : "";
    }


    // ==========================================
    // 2. DESPACHOS Y ENTREGAS
    // ==========================================

    function accionesDespacho(item) {

        const id = item.id_despacho;

        const button = (estado, texto, clase = "") => `
            <button
                class="mini-button ${clase}"
                data-dispatch-state="${estado}"
                data-id="${id}"
                type="button">
                ${texto}
            </button>
        `;

        switch (item.estado) {

            case "preparando":

                return `
                    <div class="action-group">
                        ${button(
                            "despachado",
                            "Marcar despachado",
                            "accept"
                        )}
                        ${button(
                            "con_novedad",
                            "Novedad",
                            "reject"
                        )}
                    </div>
                `;

            case "despachado":

                return `
                    <div class="action-group">
                        ${button(
                            "en_transito",
                            "En tránsito",
                            "info-action"
                        )}
                        ${button(
                            "entregado",
                            "Confirmar entrega",
                            "accept"
                        )}
                        ${button(
                            "con_novedad",
                            "Novedad",
                            "reject"
                        )}
                    </div>
                `;

            case "en_transito":

                return `
                    <div class="action-group">
                        ${button(
                            "entregado",
                            "Confirmar entrega",
                            "accept"
                        )}
                        ${button(
                            "con_novedad",
                            "Novedad",
                            "reject"
                        )}
                    </div>
                `;

            case "con_novedad":

                return `
                    <div class="action-group">
                        ${button(
                            "en_transito",
                            "Reanudar envío",
                            "info-action"
                        )}
                    </div>
                `;

            default:

                return `
                    <span class="muted-text">
                        Entrega finalizada
                    </span>
                `;
        }
    }


    function renderDespachos() {

        const body = $("#dispatchTableBody");

        const activos = state.despachos.filter(
            (item) => item.estado !== "entregado"
        );

        $("#dispatchCount").textContent = activos.length;

        if (!state.despachos.length) {

            body.innerHTML = `
                <tr>
                    <td colspan="7">

                        <div class="empty-state">

                            <span class="empty-icon">↗</span>

                            <strong>
                                Aún no hay despachos registrados
                            </strong>

                            <p>
                                Registra el primer despacho cuando exista
                                una solicitud aceptada.
                            </p>

                        </div>

                    </td>
                </tr>
            `;

            return;
        }

        body.innerHTML = state.despachos.map((item) => `

            <tr>

                <td>
                    <strong>#${item.id_despacho}</strong>

                    <small class="table-subtext">
                        ${fechaCorta(item.fecha_despacho)}
                    </small>
                </td>

                <td>
                    #${item.solicitud_id_solicitud}
                </td>

                <td>
                    ${escapeHTML(item.producto_nombre || "Producto")}
                </td>

                <td>
                    ${Number(item.cantidad_despachada)
                        .toLocaleString("es-CO")}
                </td>

                <td>
                    ${escapeHTML(item.numero_guia || "—")}
                </td>

                <td>
                    ${badgeEstado(item.estado)}
                </td>

                <td>
                    ${accionesDespacho(item)}
                </td>

            </tr>

        `).join("");
    }


    // ==========================================
    // 3. HISTORIAL DE OPERACIONES
    // ==========================================

    function renderHistorial() {

        const body = $("#historyTableBody");

        if (!state.historial.length) {

            body.innerHTML = `
                <tr>
                    <td colspan="4">

                        <div class="empty-state">

                            <strong>
                                Sin movimientos registrados
                            </strong>

                            <p>
                                Las solicitudes y despachos aparecerán aquí
                                a medida que se realicen operaciones.
                            </p>

                        </div>

                    </td>
                </tr>
            `;

            return;
        }

        body.innerHTML = state.historial.map((item) => `

            <tr>

                <td>
                    ${fechaCorta(item.fecha)}
                </td>

                <td>
                    ${escapeHTML(item.tipo)}
                </td>

                <td>

                    <strong>
                        ${escapeHTML(item.referencia)}
                    </strong>

                    <small class="table-subtext">
                        ${escapeHTML(item.detalle)}
                    </small>

                </td>

                <td>
                    ${badgeEstado(item.estado)}
                </td>

            </tr>

        `).join("");
    }


    // ==========================================
    // CARGAR INFORMACIÓN DESDE FLASK Y MYSQL
    // ==========================================

    async function cargarDatosProveedor() {

        const provider = state.proveedorActual;

        if (!provider) return;

        const id = provider.id_proveedor;

        const [
            solicitudesResult,
            despachosResult,
            historialResult
        ] = await Promise.allSettled([

            getJSON(
                `${API.solicitudes}?proveedor_id=${id}`
            ),

            getJSON(
                `${API.despachos}?proveedor_id=${id}`
            ),

            getJSON(
                `${API.proveedores}/${id}/historial`
            )

        ]);


        // Resultado de solicitudes

        if (solicitudesResult.status === "fulfilled") {

            state.solicitudes =
                Array.isArray(solicitudesResult.value)
                    ? solicitudesResult.value
                    : [];

            setFeatureStatus(
                "#requestsConnectionStatus",
                true,
                "Conectado a MySQL"
            );

        } else {

            state.solicitudes = [];

            setFeatureStatus(
                "#requestsConnectionStatus",
                false,
                "Error de conexión"
            );

            $("#requestsTableBody").innerHTML = `
                <tr>
                    <td colspan="6">
                        <div class="empty-state">

                            <strong>
                                No se pudieron cargar las solicitudes
                            </strong>

                            <p>
                                ${escapeHTML(
                                    solicitudesResult.reason.message
                                )}
                            </p>

                        </div>
                    </td>
                </tr>
            `;
        }


        // Resultado de despachos

        if (despachosResult.status === "fulfilled") {

            state.despachos =
                Array.isArray(despachosResult.value)
                    ? despachosResult.value
                    : [];

            setFeatureStatus(
                "#dispatchConnectionStatus",
                true,
                "Conectado a MySQL"
            );

        } else {

            state.despachos = [];

            setFeatureStatus(
                "#dispatchConnectionStatus",
                false,
                "Error de conexión"
            );

            $("#dispatchTableBody").innerHTML = `
                <tr>
                    <td colspan="7">
                        <div class="empty-state">

                            <strong>
                                No se pudieron cargar los despachos
                            </strong>

                            <p>
                                ${escapeHTML(
                                    despachosResult.reason.message
                                )}
                            </p>

                        </div>
                    </td>
                </tr>
            `;
        }


        // Resultado del historial

        if (historialResult.status === "fulfilled") {

            state.historial =
                Array.isArray(historialResult.value)
                    ? historialResult.value
                    : [];

            setFeatureStatus(
                "#historyConnectionStatus",
                true,
                "Historial conectado"
            );

        } else {

            state.historial = [];

            setFeatureStatus(
                "#historyConnectionStatus",
                false,
                "Error de conexión"
            );
        }


        // Actualizar las tablas

        renderSolicitudes();
        renderDespachos();
        renderHistorial();
    }


    // ==========================================
    // CAMBIAR PROVEEDOR
    // ==========================================

    async function selectProvider(id) {

        const provider = state.proveedores.find(
            (item) =>
                Number(item.id_proveedor) === Number(id)
        );

        state.proveedorActual = provider || null;

        if (!provider) return;

        sessionStorage.setItem(
            "proveedorSeleccionado",
            String(provider.id_proveedor)
        );

        renderProfile();
        renderCatalog();

        $("#requestsTableBody").innerHTML = `
            <tr>
                <td colspan="6">
                    <div class="empty-state">
                        <strong>Cargando solicitudes...</strong>
                    </div>
                </td>
            </tr>
        `;

        $("#dispatchTableBody").innerHTML = `
            <tr>
                <td colspan="7">
                    <div class="empty-state">
                        <strong>Cargando despachos...</strong>
                    </div>
                </td>
            </tr>
        `;

        await cargarDatosProveedor();
    }


    // ==========================================
    // CARGA INICIAL
    // ==========================================

    async function loadInitialData() {

        try {

            const [providers, products] = await Promise.all([

                getJSON(API.proveedores),

                getJSON(API.productos)

            ]);

            state.proveedores =
                Array.isArray(providers) ? providers : [];

            state.productos =
                Array.isArray(products) ? products : [];

            fillProductOptions();

            setConnection(
                true,
                "Conectado con MySQL"
            );

            if (!state.proveedores.length) {

                fillProviderSelector();

                $("#catalogContent").innerHTML = `
                    <div class="loading-card">
                        No existen proveedores registrados.
                    </div>
                `;

                return;
            }

            fillProviderSelector();

        } catch (error) {

            setConnection(
                false,
                "No fue posible conectar"
            );

            $("#providerSelect").innerHTML = `
                <option value="">
                    Error al cargar proveedores
                </option>
            `;

            $("#catalogContent").innerHTML = `
                <div class="loading-card">
                    No se pudieron consultar los datos.
                    Verifica MySQL y Flask.
                    ${escapeHTML(error.message)}
                </div>
            `;

            $("#profileMessage").textContent =
                "No se pudo cargar la información del proveedor.";

            $("#profileMessage").classList.add("error");
        }
    }


    // ==========================================
    // ACTUALIZAR INFORMACIÓN DEL PROVEEDOR
    // ==========================================

    async function saveProfile(event) {

        event.preventDefault();

        const provider = state.proveedorActual;

        if (!provider) {
            return notify(
                "Primero selecciona un proveedor.",
                true
            );
        }

        const message = $("#profileMessage");

        const payload = {

            nombre: $("#profileName").value.trim(),

            telefono:
                $("#profilePhone").value.trim() || null,

            correo:
                $("#profileEmail").value.trim() || null,

            direccion:
                $("#profileAddress").value.trim() || null,

            producto_id_producto:
                $("#profileProduct").value
                    ? Number($("#profileProduct").value)
                    : null
        };

        if (!payload.nombre) {

            message.textContent = "El nombre es obligatorio.";

            message.classList.add("error");

            return;
        }

        try {

            const updated = await getJSON(
                `${API.proveedores}/${provider.id_proveedor}`,
                {
                    method: "PUT",
                    body: JSON.stringify(payload)
                }
            );

            state.proveedores = state.proveedores.map(
                (item) =>
                    Number(item.id_proveedor) ===
                    Number(updated.id_proveedor)
                        ? updated
                        : item
            );

            state.proveedorActual = updated;

            $("#providerSelect").value =
                String(updated.id_proveedor);

            renderProfile();
            renderCatalog();

            message.textContent =
                "Cambios guardados correctamente.";

            notify(
                "Información del proveedor actualizada en MySQL."
            );

            await cargarDatosProveedor();

        } catch (error) {

            message.textContent = error.message;

            message.classList.add("error");

            notify(
                "No fue posible guardar los cambios.",
                true
            );
        }
    }


    // ==========================================
    // ACEPTAR O RECHAZAR SOLICITUD
    // ==========================================

    async function responderSolicitud(id, estado) {

        let motivo = null;

        if (estado === "rechazada") {

            motivo = window.prompt(
                "Indica el motivo del rechazo:"
            );

            if (motivo === null) return;

            motivo = motivo.trim();

            if (!motivo) {

                return notify(
                    "Debes indicar el motivo del rechazo.",
                    true
                );
            }

        } else if (
            !window.confirm(
                "¿Confirmas que deseas aceptar esta solicitud?"
            )
        ) {

            return;
        }

        try {

            await getJSON(
                `${API.solicitudes}/${id}/estado`,
                {
                    method: "PATCH",

                    body: JSON.stringify({
                        estado,
                        motivo_rechazo: motivo
                    })
                }
            );

            notify(
                estado === "aceptada"
                    ? "Solicitud aceptada correctamente."
                    : "Solicitud rechazada correctamente."
            );

            await cargarDatosProveedor();

        } catch (error) {

            notify(error.message, true);
        }
    }


    // ==========================================
    // REGISTRAR DESPACHO
    // ==========================================

    async function crearDespacho(event) {

        event.preventDefault();

        const solicitudId =
            Number($("#dispatchRequest").value);

        const cantidad =
            Number($("#dispatchQuantity").value);

        const message = $("#dispatchMessage");

        if (
            !solicitudId ||
            !Number.isInteger(cantidad) ||
            cantidad <= 0
        ) {

            message.textContent =
                "Selecciona una solicitud e indica una cantidad válida.";

            message.classList.add("error");

            return;
        }

        const payload = {

            solicitud_id_solicitud: solicitudId,

            cantidad_despachada: cantidad,

            fecha_entrega_estimada:
                $("#dispatchDueDate").value || null,

            numero_guia:
                $("#dispatchGuide").value.trim() || null,

            transportadora:
                $("#dispatchCarrier").value.trim() || null,

            observaciones:
                $("#dispatchObservations").value.trim() || null
        };

        try {

            await getJSON(
                API.despachos,
                {
                    method: "POST",
                    body: JSON.stringify(payload)
                }
            );

            $("#dispatchForm").reset();

            message.textContent =
                "Despacho registrado correctamente.";

            message.classList.remove("error");

            notify(
                "Despacho guardado en MySQL."
            );

            await cargarDatosProveedor();

        } catch (error) {

            message.textContent = error.message;

            message.classList.add("error");

            notify(
                "No fue posible registrar el despacho.",
                true
            );
        }
    }


    // ==========================================
    // ACTUALIZAR ESTADO Y CONFIRMAR ENTREGA
    // ==========================================

    async function actualizarEstadoDespacho(id, estado) {

        const entregado = estado === "entregado";

        const mensaje = entregado

            ? "¿Confirmas que el restaurante recibió este despacho? Esta acción cierra el despacho."

            : `¿Deseas cambiar el estado del despacho a "${labelEstado(estado)}"?`;

        if (!window.confirm(mensaje)) return;

        try {

            const url = entregado

                ? `${API.despachos}/${id}/confirmar-entrega`

                : `${API.despachos}/${id}/estado`;

            const options = entregado

                ? {
                    method: "POST"
                }

                : {
                    method: "PATCH",
                    body: JSON.stringify({ estado })
                };

            await getJSON(url, options);

            notify(
                entregado
                    ? "Entrega confirmada correctamente."
                    : "Estado del despacho actualizado."
            );

            await cargarDatosProveedor();

        } catch (error) {

            notify(error.message, true);
        }
    }


    // ==========================================
    // EVENTOS DE LA INTERFAZ
    // ==========================================

    function bindEvents() {

        // Navegación

        $$(".nav-link").forEach((button) => {

            button.addEventListener(
                "click",
                () => changeView(button.dataset.view)
            );

        });


        // Cambio de proveedor

        $("#providerSelect").addEventListener(
            "change",
            (event) => selectProvider(event.target.value)
        );


        // Formularios

        $("#profileForm").addEventListener(
            "submit",
            saveProfile
        );

        $("#dispatchForm").addEventListener(
            "submit",
            crearDespacho
        );


        // Menú para celular

        $("#mobileMenu").addEventListener(
            "click",
            () => $("#sidebar").classList.toggle("open")
        );


        // Búsqueda y filtros

        $("#requestSearch").addEventListener(
            "input",
            renderSolicitudes
        );

        $("#requestStatusFilter").addEventListener(
            "change",
            renderSolicitudes
        );


        // Actualizar tablas

        $("#refreshRequests").addEventListener(
            "click",
            cargarDatosProveedor
        );

        $("#refreshDispatches").addEventListener(
            "click",
            cargarDatosProveedor
        );


        // Acciones de solicitudes

        $("#requestsTableBody").addEventListener(
            "click",
            (event) => {

                const button = event.target.closest(
                    "[data-request-action]"
                );

                if (button) {

                    responderSolicitud(
                        Number(button.dataset.id),
                        button.dataset.requestAction
                    );

                }
            }
        );


        // Acciones de despachos

        $("#dispatchTableBody").addEventListener(
            "click",
            (event) => {

                const button = event.target.closest(
                    "[data-dispatch-state]"
                );

                if (button) {

                    actualizarEstadoDespacho(
                        Number(button.dataset.id),
                        button.dataset.dispatchState
                    );

                }
            }
        );


        // Cantidad máxima según solicitud

        $("#dispatchRequest").addEventListener(
            "change",
            () => {

                const selected = state.solicitudes.find(
                    (item) =>
                        Number(item.id_solicitud) ===
                        Number($("#dispatchRequest").value)
                );

                $("#dispatchQuantity").max = selected
                    ? selected.cantidad_pendiente_despacho
                    : "";
            }
        );
    }


    // ==========================================
    // INICIAR APLICACIÓN
    // ==========================================

    document.addEventListener(
        "DOMContentLoaded",
        () => {

            bindEvents();

            loadInitialData();

        }
    );

})();
