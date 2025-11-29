/* game_logic.js - Murder.Ai Frontend Logic */

console.log("🕵️ Murder.Ai Detective Interface Initialized");

// State
let gameState = {
    suspects: [],
    evidence: [],
    chatLog: [],
    currentSuspect: null
};

// --- Bridge: Communication with Parent (Python/Gradio) ---

// We now use direct API calls for reliability
async function sendAction(action, data) {
    // console.log("📤 Sending API request:", action, data);
    try {
        const response = await fetch('/api/bridge', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action, data }),
        });
        
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        
        const result = await response.json();
        // console.log("📥 API Response:", result);
        
        if (result && result.action) {
            handleServerMessage(result);
        }
    } catch (e) {
        console.error("Bridge Error:", e);
    }
}

// Keep listener for any future server-pushed events (if we add sockets later)
window.addEventListener('message', function(event) {
    const { action, data } = event.data;
    if (action) handleServerMessage({ action, data });
});

function handleServerMessage(message) {
    const { action, data } = message;
    switch(action) {
        case 'init_game':
            initializeGame(data);
            break;
        case 'update_chat':
            addChatMessage(data.role, data.content, data.name);
            break;
        case 'add_evidence':
            addEvidenceToBoard(data);
            break;
        case 'update_status':
            updateStatus(data);
            break;
        case 'game_over':
            triggerGameOver(data);
            break;
        default:
            console.warn("Unknown action:", action);
    }
}

// --- Game Logic ---

function initializeGame(data) {
    gameState = data;
    renderSuspects();
    document.getElementById('loading-overlay').style.opacity = 0;
    setTimeout(() => {
        document.getElementById('loading-overlay').style.display = 'none';
    }, 1000);
    
    addChatMessage('system', `CASE LOADED: ${data.scenario.title}`);
    addChatMessage('system', `VICTIM: ${data.scenario.victim.name}`);
    
    // Update UI stats
    document.getElementById('round-display').innerText = `${data.round}/5`;
    document.getElementById('points-display').innerText = data.points;
    
    renderCaseFile(data.scenario);
}

function renderCaseFile(scenario) {
    const victim = scenario.victim;
    const details = `
        <div style="border-bottom: 2px solid black; margin-bottom: 5px; padding-bottom: 5px;"><strong>POLICE REPORT</strong></div>
        <div><strong>CASE:</strong> ${scenario.title}</div>
        <div><strong>VICTIM:</strong> ${victim.name} (${victim.age})</div>
        <div><strong>OCCUPATION:</strong> ${victim.occupation}</div>
        <div><strong>TIME OF DEATH:</strong> ${victim.time_of_death}</div>
        <div><strong>LOCATION:</strong> ${victim.location || "Unknown"}</div>
    `;
    
    addEvidenceToBoard({
        title: "CASE FILE #A47",
        description: details,
        type: "file"
    }, 20, 20);
}

// --- UI Rendering: Suspects ---

function renderSuspects() {
    const container = document.getElementById('suspect-files');
    container.innerHTML = '<div class="folder-label">SUSPECTS</div>';
    
    if (!gameState.scenario || !gameState.scenario.suspects) return;

    gameState.scenario.suspects.forEach(suspect => {
        const card = document.createElement('div');
        card.className = 'suspect-card';
        card.dataset.id = suspect.id;
        card.onclick = () => selectSuspect(suspect.id);
        
        // Placeholder Avatar (Initials)
        const initials = suspect.name.split(' ').map(n => n[0]).join('');
        
        card.innerHTML = `
            <div class="suspect-img">${initials}</div>
            <div class="suspect-name">${suspect.name}</div>
            <div class="suspect-role">${suspect.role}</div>
            <div class="suspect-phone" title="Click to copy" onclick="event.stopPropagation(); copyToClipboard('${suspect.phone_number}')">
                📞 ${suspect.phone_number} 📋
            </div>
            <div class="status-stamp"></div>
        `;
        
        container.appendChild(card);
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert("Copied: " + text);
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}

function selectSuspect(suspectId) {
    gameState.currentSuspect = suspectId;
    const suspect = gameState.scenario.suspects.find(s => s.id === suspectId);
    
    // Highlight visual
    document.querySelectorAll('.suspect-card').forEach(el => {
        el.style.border = el.dataset.id === suspectId ? '2px solid red' : 'none';
    });
    
    addChatMessage('system', `Selected suspect: ${suspect.name}. You may now question them.`);
    sendAction('select_suspect', { suspect_id: suspectId });
}

// --- UI Rendering: Chat ---

function addChatMessage(role, text, name="System") {
    const log = document.getElementById('chat-log');
    const msg = document.createElement('div');
    
    let className = 'system';
    if (role === 'user' || role === 'detective') className = 'detective';
    if (role === 'assistant' || role === 'suspect') className = 'suspect';
    
    msg.className = `chat-message ${className}`;
    
    // Format: NAME: Message
    const displayName = name ? name.toUpperCase() : role.toUpperCase();
    msg.innerHTML = `<strong>${displayName}:</strong> ${text}`;
    
    log.appendChild(msg);
    log.scrollTop = log.scrollHeight;
}

function sendUserMessage() {
    const input = document.getElementById('chat-input');
    const text = input.value.trim();
    
    if (!text) return;
    
    if (!gameState.currentSuspect) {
        alert("Select a suspect first!");
        return;
    }
    
    addChatMessage('detective', text, "YOU");
    sendAction('chat_message', { 
        suspect_id: gameState.currentSuspect,
        message: text 
    });
    
    input.value = '';
}

// --- UI Rendering: Evidence Board ---

function addEvidenceToBoard(evidenceData, fixedX = null, fixedY = null) {
    const board = document.getElementById('evidence-board');
    
    const item = document.createElement('div');
    item.className = 'evidence-item';
    if (evidenceData.type === 'file') {
        item.classList.add('case-file');
        item.innerHTML = evidenceData.description;
    } else {
        item.innerHTML = `
            <strong>${evidenceData.title || "Evidence"}</strong><br>
            ${evidenceData.description || "No details."}
        `;
    }
    
    // Placement
    let x, y;
    if (fixedX !== null && fixedY !== null) {
        x = fixedX;
        y = fixedY;
        item.style.transform = 'rotate(-2deg)'; // Slight tilt for files
    } else {
        x = Math.floor(Math.random() * (board.clientWidth - 200));
        y = Math.floor(Math.random() * (board.clientHeight - 100));
        item.style.transform = `rotate(${Math.random() * 10 - 5}deg)`;
    }
    
    item.style.left = x + 'px';
    item.style.top = y + 'px';
    
    // Make draggable (simple implementation)
    makeDraggable(item);
    
    board.appendChild(item);
    
    // Play sound effect (optional)
}

function makeDraggable(elmnt) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    elmnt.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
        // Bring to front
        elmnt.style.zIndex = 100;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
        elmnt.style.zIndex = 10;
    }
}

// --- Tools ---

function useTool(toolName) {
    const input = prompt(`Enter input for ${toolName} (e.g., phone number):`);
    if (input) {
        sendAction('use_tool', { tool: toolName, input: input });
    }
}

// --- Listeners ---

document.getElementById('send-btn').addEventListener('click', sendUserMessage);
document.getElementById('chat-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendUserMessage();
    }
});

// Tool Buttons
document.getElementById('tool-map').onclick = () => useTool('get_location');
document.getElementById('tool-camera').onclick = () => useTool('get_footage');
document.getElementById('tool-phone').onclick = () => useTool('call_alibi');
document.getElementById('tool-dna').onclick = () => useTool('get_dna_test');

// Notify Parent that we are ready (Retry loop)
console.log("📡 Attempting to connect to game server...");
const handshakeInterval = setInterval(() => {
    if (gameState.scenario) {
        clearInterval(handshakeInterval);
        console.log("✅ Connection established.");
    } else {
        console.log("📡 Sending 'ready' signal...");
        sendAction('ready', {});
    }
}, 2000);

// Immediate first try
sendAction('ready', {});
