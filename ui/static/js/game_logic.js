/* game_logic.js - Murder.Ai Frontend Logic */

console.log("🕵️ Murder.Ai Detective Interface Initialized");

// State
let gameState = {
    suspects: [],
    evidence: [],
    chatLog: [],
    currentSuspect: null,
    nextEvidenceSlot: 0 // Track grid position for new cards
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
            // Return result for local handling if needed
            if (result.action === 'tool_error') {
                return result; 
            }
            handleServerMessage(result);
            return result;
        }
    } catch (e) {
        console.error("Bridge Error:", e);
        return { action: 'error', message: e.message };
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
        case 'tool_error':
            showNotification("❌ " + data.message);
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
    
    // Auto-scroll slightly to hint at overflow
    setTimeout(() => {
        container.scrollTop = 40;
    }, 500);
}

// --- Modal & Notifications ---

function showNotification(message) {
    const toast = document.getElementById('notification-toast');
    toast.innerText = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification("COPIED: " + text);
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}

function selectSuspect(suspectId) {
    gameState.currentSuspect = suspectId;
    const suspect = gameState.scenario.suspects.find(s => s.id === suspectId);
    
    // Highlight visual
    document.querySelectorAll('.suspect-card').forEach(el => {
        if (el.dataset.id === suspectId) {
            el.classList.add('selected');
        } else {
            el.classList.remove('selected');
        }
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

function addEvidenceToBoard(evidenceData) {
    const board = document.getElementById('evidence-board');
    
    // Grouping Logic
    let targetCard = null;
    
    if (evidenceData.suspect_id) {
        // Per-suspect evidence
        targetCard = document.querySelector(`.evidence-item[data-suspect-id="${evidenceData.suspect_id}"]`);
    } else if (evidenceData.type !== 'file') {
        // General evidence (e.g. footage) -> goes to Case File
        targetCard = document.querySelector(`.evidence-item[data-case-file="true"]`);
    }

    if (targetCard) {
        const contentDiv = targetCard.querySelector('.evidence-content') || targetCard; // Case file might not have .evidence-content wrapper
        
        const newEntry = document.createElement('div');
        newEntry.style.marginTop = "10px";
        newEntry.style.borderTop = "1px dashed #888";
        newEntry.style.paddingTop = "5px";
        newEntry.innerHTML = `
            <div style="font-size:0.9em; font-weight:bold; color:#555;">${evidenceData.title}</div>
            ${evidenceData.html_content || evidenceData.description}
        `;
        contentDiv.appendChild(newEntry);
        
        // Flash effect
        targetCard.style.backgroundColor = "#fff";
        setTimeout(() => targetCard.style.backgroundColor = evidenceData.suspect_id ? "var(--paper-color)" : "#e8dcc8", 300);
        
        return;
    }

    const item = document.createElement('div');
    item.className = 'evidence-item';
    item.style.transform = `rotate(${Math.random() * 4 - 2}deg)`; // Slight random tilt
    
    if (evidenceData.suspect_id) {
        item.dataset.suspectId = evidenceData.suspect_id;
    }

    if (evidenceData.type === 'file') {
        item.classList.add('case-file');
        item.dataset.caseFile = "true";
        item.innerHTML = evidenceData.description;
    } else {
        // Standard Card Format
        let header = evidenceData.title || "Evidence";
        if (evidenceData.suspect_name) {
            header = `📌 ${evidenceData.suspect_name}`;
        }
        
        item.innerHTML = `
            <div style="border-bottom: 2px solid var(--ink-color); margin-bottom: 5px; font-weight: bold;">${header}</div>
            <div class="evidence-content">
                ${evidenceData.suspect_name ? `<div style="font-size:0.9em; font-weight:bold; color:#555;">${evidenceData.title}</div>` : ''}
                ${evidenceData.html_content || evidenceData.description}
            </div>
        `;
    }
    
    // No manual x/y placement. CSS Flexbox handles it.
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
        
        // If element is still relative (in grid), snap it to absolute at current position
        if (window.getComputedStyle(elmnt).position !== 'absolute') {
            const rect = elmnt.getBoundingClientRect();
            const parentRect = elmnt.parentElement.getBoundingClientRect();
            
            elmnt.style.position = 'absolute';
            elmnt.classList.add('absolute-positioned');
            elmnt.style.left = (rect.left - parentRect.left + elmnt.parentElement.scrollLeft) + 'px';
            elmnt.style.top = (rect.top - parentRect.top + elmnt.parentElement.scrollTop) + 'px';
            elmnt.style.width = rect.width + 'px'; // Maintain width
            elmnt.style.margin = '0'; // Remove flex gap margins
        }

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

let pendingTool = null;

function useTool(toolName) {
    pendingTool = toolName;
    const modal = document.getElementById('tool-modal');
    const input = document.getElementById('modal-input');
    const promptText = document.getElementById('modal-prompt-text');
    
    const section2 = document.getElementById('modal-section-2');
    const input2 = document.getElementById('modal-input-2');
    const promptText2 = document.getElementById('modal-prompt-text-2');
    
    // Reset
    section2.style.display = 'none';
    input.value = '';
    input2.value = '';
    
    // Custom prompts
    if (toolName === 'get_location') {
        promptText.innerText = "Enter Target Phone Number:";
    } else if (toolName === 'call_alibi') {
        promptText.innerText = "Enter Alibi ID (Ask suspect):";
        section2.style.display = 'block';
        promptText2.innerText = "Question for Alibi:";
    } else if (toolName === 'get_dna_test') {
        promptText.innerText = "Enter Evidence ID:";
    } else if (toolName === 'get_footage') {
        promptText.innerText = "Enter Camera Location:";
    }
    
    modal.classList.add('active');
    input.focus();
}

function submitTool() {
    const input = document.getElementById('modal-input');
    const value = input.value.trim();
    const confirmBtn = document.getElementById('modal-confirm');
    
    if (!pendingTool) return;
    
    let payload = null;
    
    if (pendingTool === 'call_alibi') {
        const input2 = document.getElementById('modal-input-2');
        const value2 = input2.value.trim();
        
        if (value && value2) {
            payload = { 
                tool: pendingTool, 
                alibi_id: value,
                question: value2
            };
        } else {
            showModalError("Both fields are required.");
            return;
        }
    } else {
        if (value) {
            payload = { tool: pendingTool, input: value };
        }
    }
    
    if (payload) {
        // Loading state
        confirmBtn.innerText = "PROCESSING...";
        confirmBtn.disabled = true;
        
        sendAction('use_tool', payload).then(result => {
            confirmBtn.innerText = "SUBMIT";
            confirmBtn.disabled = false;
            
            if (result && result.action === 'tool_error') {
                showModalError(result.data.message);
            } else {
                closeModal();
            }
        });
    }
}

function showModalError(msg) {
    let errDiv = document.getElementById('modal-error');
    if (!errDiv) {
        errDiv = document.createElement('div');
        errDiv.id = 'modal-error';
        errDiv.style.color = 'red';
        errDiv.style.marginTop = '10px';
        errDiv.style.textAlign = 'right';
        errDiv.style.fontWeight = 'bold';
        document.querySelector('.modal-content').appendChild(errDiv);
    }
    errDiv.innerText = msg;
}

function closeModal() {
    document.getElementById('tool-modal').classList.remove('active');
    pendingTool = null;
    const errDiv = document.getElementById('modal-error');
    if (errDiv) errDiv.innerText = ''; 
}

// --- Listeners ---

document.getElementById('modal-cancel').onclick = closeModal;
document.getElementById('modal-confirm').onclick = submitTool;
document.getElementById('modal-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') submitTool();
});

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
