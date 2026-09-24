const homeView = document.getElementById("home-view");
const listsView = document.getElementById("lists-view");
const alarmsView = document.getElementById("alarms-view");

const listsButton = document.getElementById("lists-button");
const alarmsButton = document.getElementById("alarms-button");

const listsBackButton = document.getElementById("lists-back-button");
const alarmsBackButton = document.getElementById("alarms-back-button");

const listsContainer = document.getElementById("lists-container");
const alarmsContainer = document.getElementById("alarms-container");

const createListForm = document.getElementById("create-list-form");
const newListName = document.getElementById("new-list-name");
const createListButton = document.getElementById("create-list-button");

const createAlarmForm = document.getElementById("create-alarm-form");
const newAlarmTime = document.getElementById("new-alarm-time");
const createAlarmButton = document.getElementById("create-alarm-button");
const alarmToneSelect = document.getElementById("alarm-tone-select");
const alarmTypeSelect = document.getElementById(
    "alarm-type-select"
);
const previewAlarmToneButton = document.getElementById(
    "preview-alarm-tone-button"
);
const snoozeAlarmButton = document.getElementById(
    "snooze-alarm-button"
);
const stopAlarmButton = document.getElementById(
    "stop-alarm-button"
);


async function checkSaturnStatus() {
    const status = document.getElementById("status");

    try {
        const response = await fetch("/api/health");

        if (!response.ok) {
            throw new Error("Health request failed.");
        }

        const data = await response.json();

        if (data.success && data.status === "online") {
            status.textContent = "SATURN Online";
            status.className = "status status-online";
            return;
        }

        throw new Error("SATURN reported offline.");
    } catch (error) {
        status.textContent = "SATURN Offline";
        status.className = "status status-offline";
    }
}


function hideAllViews() {
    homeView.classList.add("hidden");
    listsView.classList.add("hidden");
    alarmsView.classList.add("hidden");
    chatView.classList.add("hidden");
}


function showHome() {
    hideAllViews();
    homeView.classList.remove("hidden");
}


async function showLists() {
    hideAllViews();
    listsView.classList.remove("hidden");

    await loadLists();
}


async function loadAlarmTones() {
    const response = await fetch(
        "/api/alarm-tones",
        {
            cache: "no-store",
        }
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load alarm tones."
        );
    }

    const result = await response.json();
    const tones = Array.isArray(result.tones)
        ? result.tones
        : [];
    const defaultTone = (
        result.default_tone
        || "Saturn Alarm 1"
    );

    const previousValue = alarmToneSelect.value;

    alarmToneSelect.dataset.defaultTone = defaultTone;
    alarmToneSelect.replaceChildren();

    const defaultOption = document.createElement(
        "option"
    );
    defaultOption.value = "";
    defaultOption.textContent = (
        `${defaultTone} (Default)`
    );
    alarmToneSelect.appendChild(defaultOption);

    for (const tone of tones) {
        if (tone.name === defaultTone) {
            continue;
        }
        const option = document.createElement(
            "option"
        );

        option.value = tone.name;
        option.textContent = tone.name;
        option.dataset.filename = tone.filename;

        alarmToneSelect.appendChild(option);
    }

    if (
        Array.from(alarmToneSelect.options).some(
            (option) => option.value === previousValue
        )
    ) {
        alarmToneSelect.value = previousValue;
    }
}


function getSelectedAlarmToneName() {
    return (
        alarmToneSelect.value
        || alarmToneSelect.dataset.defaultTone
        || "Saturn Alarm 1"
    );
}


async function previewSelectedAlarmTone() {
    const toneName = getSelectedAlarmToneName();

    previewAlarmToneButton.disabled = true;

    try {
        const audio = new Audio(
            (
                "/api/alarm-tones/"
                + encodeURIComponent(toneName)
            )
        );

        await audio.play();
    } catch (error) {
        alert(
            "SATURN could not preview that tone "
            + "on this device."
        );
    } finally {
        previewAlarmToneButton.disabled = false;
    }
}


async function showAlarms() {
    hideAllViews();
    alarmsView.classList.remove("hidden");

    await Promise.all([
        loadAlarms(),
        loadAlarmTones(),
    ]);
}


async function loadLists() {
    listsContainer.innerHTML = `
        <p class="loading-message">
            Loading lists...
        </p>
    `;

    try {
        const response = await fetch("/api/lists");

        if (!response.ok) {
            throw new Error("List request failed.");
        }

        const data = await response.json();

        if (!data.success || !data.result?.success) {
            throw new Error("SATURN could not retrieve lists.");
        }

        renderLists(data.result.lists);
    } catch (error) {
        listsContainer.innerHTML = `
            <p class="error-message">
                Unable to load SATURN lists.
            </p>
        `;
    }
}


async function createList(name) {
    const cleanName = name.trim();

    if (!cleanName) {
        return;
    }

    const response = await fetch(
        "/api/lists",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: cleanName,
            }),
        }
    );

    if (!response.ok) {
        throw new Error("Create list request failed.");
    }

    const data = await response.json();

    if (!data.success || !data.result?.success) {
        throw new Error("SATURN could not create the list.");
    }

    await loadLists();
}


async function addListItem(listName, item) {
    const cleanItem = item.trim();

    if (!cleanItem) {
        return;
    }

    const response = await fetch(
        `/api/lists/${encodeURIComponent(listName)}/items`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                item: cleanItem,
            }),
        }
    );

    if (!response.ok) {
        throw new Error("Add item request failed.");
    }

    const data = await response.json();

    if (!data.success || !data.result?.success) {
        throw new Error("SATURN could not add the item.");
    }

    await loadLists();
}


async function removeListItem(listName, item) {
    const response = await fetch(
        `/api/lists/${encodeURIComponent(listName)}/items/${encodeURIComponent(item)}`,
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        throw new Error("Remove item request failed.");
    }

    const data = await response.json();

    if (!data.success || !data.result?.success) {
        throw new Error("SATURN could not remove the item.");
    }

    await loadLists();
}


async function clearList(listName) {
    const response = await fetch(
        `/api/lists/${encodeURIComponent(listName)}/items`,
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        throw new Error("Clear list request failed.");
    }

    const data = await response.json();

    if (!data.success || !data.result?.success) {
        throw new Error("SATURN could not clear the list.");
    }

    await loadLists();
}


async function deleteList(listName) {
    const response = await fetch(
        `/api/lists/${encodeURIComponent(listName)}`,
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        throw new Error("Delete list request failed.");
    }

    const data = await response.json();

    if (!data.success || !data.result?.success) {
        throw new Error("SATURN could not delete the list.");
    }

    await loadLists();
}


function renderLists(lists) {
    listsContainer.innerHTML = "";

    if (!lists.length) {
        listsContainer.innerHTML = `
            <p class="empty-list">
                You don't have any lists yet.
            </p>
        `;

        return;
    }

    for (const list of lists) {
        const card = document.createElement("section");
        card.className = "list-card";

        const header = document.createElement("div");
        header.className = "list-card-header";

        const heading = document.createElement("h3");
        heading.textContent = list.display_name;

        const controls = document.createElement("div");
        controls.className = "list-controls";

        const clearButton = document.createElement("button");
        clearButton.className = "list-control-button";
        clearButton.type = "button";
        clearButton.textContent = "Clear";

        clearButton.addEventListener(
            "click",
            async () => {
                if (!list.items.length) {
                    return;
                }

                if (!confirm(
                    `Clear every item from ${list.display_name}?`
                )) {
                    return;
                }

                clearButton.disabled = true;

                try {
                    await clearList(list.name);
                } catch (error) {
                    alert("SATURN could not clear that list.");
                    clearButton.disabled = false;
                }
            }
        );

        const deleteButton = document.createElement("button");
        deleteButton.className = "list-control-button delete-list-button";
        deleteButton.type = "button";
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener(
            "click",
            async () => {
                if (!confirm(
                    `Delete the ${list.display_name} list?`
                )) {
                    return;
                }

                deleteButton.disabled = true;

                try {
                    await deleteList(list.name);
                } catch (error) {
                    alert("SATURN could not delete that list.");
                    deleteButton.disabled = false;
                }
            }
        );

        controls.appendChild(clearButton);
        controls.appendChild(deleteButton);

        header.appendChild(heading);
        header.appendChild(controls);

        card.appendChild(header);

        if (!list.items.length) {
            const empty = document.createElement("p");

            empty.className = "empty-list";
            empty.textContent = "This list is empty.";

            card.appendChild(empty);
        } else {
            const itemList = document.createElement("ul");

            itemList.className = "list-items editable-list-items";

            for (const item of list.items) {
                const row = document.createElement("li");
                row.className = "list-item-row";

                const itemText = document.createElement("span");
                itemText.className = "list-item-text";
                itemText.textContent = item;

                const removeButton = document.createElement("button");

                removeButton.className = "remove-item-button";
                removeButton.type = "button";
                removeButton.textContent = "Remove";

                removeButton.addEventListener(
                    "click",
                    async () => {
                        removeButton.disabled = true;

                        try {
                            await removeListItem(
                                list.name,
                                item
                            );
                        } catch (error) {
                            alert(
                                "SATURN could not remove that item."
                            );

                            removeButton.disabled = false;
                        }
                    }
                );

                row.appendChild(itemText);
                row.appendChild(removeButton);

                itemList.appendChild(row);
            }

            card.appendChild(itemList);
        }

        const form = document.createElement("form");
        form.className = "add-item-form";

        const input = document.createElement("input");
        input.className = "item-input";
        input.type = "text";
        input.placeholder = "Add an item...";
        input.autocomplete = "off";

        const button = document.createElement("button");
        button.className = "add-item-button";
        button.type = "submit";
        button.textContent = "Add";

        form.appendChild(input);
        form.appendChild(button);

        form.addEventListener(
            "submit",
            async (event) => {
                event.preventDefault();

                button.disabled = true;
                input.disabled = true;

                try {
                    await addListItem(
                        list.name,
                        input.value
                    );
                } catch (error) {
                    alert(
                        "SATURN could not add that item."
                    );

                    button.disabled = false;
                    input.disabled = false;
                }
            }
        );

        card.appendChild(form);

        listsContainer.appendChild(card);
    }
}


async function loadAlarms() {
    alarmsContainer.innerHTML = `
        <p class="loading-message">
            Loading alarms...
        </p>
    `;

    try {
        const response = await fetch("/api/alarms");

        if (!response.ok) {
            throw new Error("Alarm request failed.");
        }

        const data = await response.json();

        if (!data.success || !data.result?.success) {
            throw new Error("SATURN could not retrieve alarms.");
        }

        renderAlarms(data.result.data?.alarms ?? []);
    } catch (error) {
        alarmsContainer.innerHTML = `
            <p class="error-message">
                Unable to load SATURN alarms.
            </p>
        `;
    }
}


async function createAlarm(
    time,
    tone,
    alarmType,
) {
    const cleanTime = time.trim();

    if (!cleanTime) {
        return;
    }

    const requestBody = {
        time: cleanTime,
        tone: tone || null,
        alarm_type: alarmType,
    };

    const response = await fetch(
        "/api/alarms",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(
                requestBody
            ),
        }
    );

    if (!response.ok) {
        throw new Error("Create alarm request failed.");
    }

    const data = await response.json();

    if (!data.success || !data.result?.success) {
        throw new Error("SATURN could not create the alarm.");
    }

    await loadAlarms();
}


async function controlRingingAlarm(action) {
    const response = await fetch(
        `/api/alarms/${action}`,
        {
            method: "POST",
        }
    );

    const data = await response.json();

    if (
        !response.ok
        || !data.success
        || !data.result?.success
    ) {
        throw new Error(
            data.result?.response
            ?? "SATURN could not control the alarm."
        );
    }

    return data.result;
}


async function runAlarmControl(
    action,
    button,
) {
    snoozeAlarmButton.disabled = true;
    stopAlarmButton.disabled = true;

    try {
        const result = await controlRingingAlarm(
            action
        );

        alert(
            result.response
            ?? "Alarm command completed."
        );

        await loadAlarms();
    } catch (error) {
        alert(
            error.message
            ?? "SATURN could not control the alarm."
        );
    } finally {
        snoozeAlarmButton.disabled = false;
        stopAlarmButton.disabled = false;
    }
}


async function cancelAlarm(alarmTime) {
    const response = await fetch(
        `/api/alarms/${encodeURIComponent(alarmTime)}`,
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        throw new Error("Cancel alarm request failed.");
    }

    const data = await response.json();

    if (!data.success || !data.result?.success) {
        throw new Error("SATURN could not cancel the alarm.");
    }

    await loadAlarms();
}


async function cancelAllAlarms() {
    const response = await fetch(
        "/api/alarms",
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        throw new Error("Cancel all alarms request failed.");
    }

    const data = await response.json();

    if (!data.success || !data.result?.success) {
        throw new Error("SATURN could not cancel the alarms.");
    }

    await loadAlarms();
}


function renderAlarms(alarms) {
    alarmsContainer.innerHTML = "";

    if (!alarms.length) {
        alarmsContainer.innerHTML = `
            <section class="list-card">
                <p class="empty-list">
                    You don't have any active alarms.
                </p>
            </section>
        `;

        return;
    }

    const toolbar = document.createElement("div");
    toolbar.className = "alarm-toolbar";

    const cancelAllButton = document.createElement("button");

    cancelAllButton.className =
        "list-control-button delete-list-button";

    cancelAllButton.type = "button";
    cancelAllButton.textContent = "Cancel All Alarms";

    cancelAllButton.addEventListener(
        "click",
        async () => {
            if (!confirm("Cancel all active alarms?")) {
                return;
            }

            cancelAllButton.disabled = true;

            try {
                await cancelAllAlarms();
            } catch (error) {
                alert(
                    "SATURN could not cancel all alarms."
                );

                cancelAllButton.disabled = false;
            }
        }
    );

    toolbar.appendChild(cancelAllButton);
    alarmsContainer.appendChild(toolbar);

    for (const alarm of alarms) {
        const card = document.createElement("section");
        card.className = "list-card";

        const header = document.createElement("div");
        header.className = "list-card-header";

        const information = document.createElement("div");

        const heading = document.createElement("h3");

        const trigger = new Date(alarm.trigger_at);

        const displayTime = trigger.toLocaleTimeString(
            [],
            {
                hour: "numeric",
                minute: "2-digit",
            }
        );

        heading.textContent = displayTime;

        const date = document.createElement("p");
        date.className = "empty-list";

        date.textContent = trigger.toLocaleDateString(
            [],
            {
                weekday: "long",
                month: "long",
                day: "numeric",
            }
        );

        information.appendChild(heading);
        information.appendChild(date);

        const cancelButton = document.createElement("button");

        cancelButton.className =
            "list-control-button delete-list-button";

        cancelButton.type = "button";
        cancelButton.textContent = "Cancel";

        cancelButton.addEventListener(
            "click",
            async () => {
                if (!confirm(
                    `Cancel the ${displayTime} alarm?`
                )) {
                    return;
                }

                cancelButton.disabled = true;

                try {
                    await cancelAlarm(displayTime);
                } catch (error) {
                    alert(
                        "SATURN could not cancel that alarm."
                    );

                    cancelButton.disabled = false;
                }
            }
        );

        header.appendChild(information);
        header.appendChild(cancelButton);

        card.appendChild(header);
        alarmsContainer.appendChild(card);
    }
}


createListForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const name = newListName.value.trim();

        if (!name) {
            return;
        }

        createListButton.disabled = true;
        newListName.disabled = true;

        try {
            await createList(name);
            newListName.value = "";
        } catch (error) {
            alert("SATURN could not create that list.");
        } finally {
            createListButton.disabled = false;
            newListName.disabled = false;
            newListName.focus();
        }
    }
);


previewAlarmToneButton.addEventListener(
    "click",
    previewSelectedAlarmTone
);


snoozeAlarmButton.addEventListener(
    "click",
    async () => {
        await runAlarmControl(
            "snooze",
            snoozeAlarmButton,
        );
    }
);


stopAlarmButton.addEventListener(
    "click",
    async () => {
        await runAlarmControl(
            "stop",
            stopAlarmButton,
        );
    }
);


createAlarmForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const time = newAlarmTime.value.trim();
        const tone = alarmToneSelect.value;
        const alarmType = alarmTypeSelect.value;

        if (!time) {
            return;
        }

        createAlarmButton.disabled = true;
        newAlarmTime.disabled = true;
        alarmToneSelect.disabled = true;
        alarmTypeSelect.disabled = true;

        try {
            await createAlarm(
                time,
                tone,
                alarmType,
            );
            newAlarmTime.value = "";
        } catch (error) {
            alert("SATURN could not set that alarm.");
        } finally {
            createAlarmButton.disabled = false;
            newAlarmTime.disabled = false;
            alarmToneSelect.disabled = false;
            alarmTypeSelect.disabled = false;
            newAlarmTime.focus();
        }
    }
);


listsButton.addEventListener(
    "click",
    showLists
);

alarmsButton.addEventListener(
    "click",
    showAlarms
);

listsBackButton.addEventListener(
    "click",
    showHome
);

alarmsBackButton.addEventListener(
    "click",
    showHome
);


const chatView = document.getElementById("chat-view");
const chatButton = document.getElementById("chat-button");
const chatBackButton = document.getElementById(
    "chat-back-button"
);
const chatMessages = document.getElementById(
    "chat-messages"
);
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatSendButton = document.getElementById(
    "chat-send-button"
);

const SATURN_CHAT_SESSION_KEY =
    "saturn-conversation-session-id";


function createConversationSessionId() {
    if (
        window.crypto
        && typeof window.crypto.randomUUID === "function"
    ) {
        return `pwa-${window.crypto.randomUUID()}`;
    }

    return (
        `pwa-${Date.now()}-`
        + Math.random().toString(16).slice(2)
    );
}


function getConversationSessionId() {
    let sessionId = localStorage.getItem(
        SATURN_CHAT_SESSION_KEY
    );

    if (!sessionId || sessionId.length > 128) {
        sessionId = createConversationSessionId();

        localStorage.setItem(
            SATURN_CHAT_SESSION_KEY,
            sessionId
        );
    }

    return sessionId;
}


function showChat() {
    hideAllViews();
    chatView.classList.remove("hidden");
    chatInput.focus();
}


function appendChatMessage(
    speaker,
    message,
    messageClass,
) {
    const messageElement = document.createElement("div");
    messageElement.className =
        `chat-message ${messageClass}`;

    const speakerElement = document.createElement("strong");
    speakerElement.textContent = speaker;

    const contentElement = document.createElement("p");
    contentElement.textContent = message;

    messageElement.appendChild(speakerElement);
    messageElement.appendChild(contentElement);
    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


async function sendChatMessage(message) {
    const cleanMessage = message.trim();

    if (!cleanMessage) {
        return;
    }

    appendChatMessage(
        "You",
        cleanMessage,
        "user-message",
    );

    chatSendButton.disabled = true;
    chatInput.disabled = true;

    try {
        const response = await fetch(
            "/api/query",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(
                    {
                        text: cleanMessage,
                        session_id:
                            getConversationSessionId(),
                    }
                ),
            }
        );

        if (!response.ok) {
            throw new Error(
                "SATURN query request failed."
            );
        }

        const data = await response.json();
        const reply = data.result?.response;

        if (
            !data.success
            || typeof reply !== "string"
            || !reply.trim()
        ) {
            throw new Error(
                "SATURN returned an invalid response."
            );
        }

        appendChatMessage(
            "SATURN",
            reply,
            "assistant-message",
        );
    } catch (error) {
        appendChatMessage(
            "SATURN",
            "I could not complete that request.",
            "error-chat-message",
        );
    } finally {
        chatSendButton.disabled = false;
        chatInput.disabled = false;
        chatInput.focus();
    }
}


chatForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const message = chatInput.value.trim();

        if (!message) {
            return;
        }

        chatInput.value = "";

        await sendChatMessage(message);
    }
);


chatButton.addEventListener(
    "click",
    showChat
);

chatBackButton.addEventListener(
    "click",
    showHome
);


checkSaturnStatus();


if ("serviceWorker" in navigator) {
    window.addEventListener(
        "load",
        async () => {
            try {
                await navigator.serviceWorker.register(
                    "/app/service-worker.js",
                    {
                        scope: "/",
                    }
                );

                console.log(
                    "SATURN service worker registered."
                );
            } catch (error) {
                console.error(
                    "SATURN service worker registration failed:",
                    error
                );
            }
        }
    );
}
