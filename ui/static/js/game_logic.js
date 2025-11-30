/* game_logic.js - Murder.Ai Frontend Logic */

console.log("🕵️ Murder.Ai Detective Interface Initialized");

// State
let gameState = {
    suspects: [],
    evidence: [],
    chatLog: [],
    currentSuspect: null,
    nextEvidenceSlot: 0, // Track grid position for new cards
    availableCameras: [],
    dnaMap: {},
    unlockedEvidence: [],
    imageMetadata: []
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
            if (data.updated_points !== undefined) {
                document.getElementById('points-display').innerText = data.updated_points;
            }
            // console.log("Evidence Data:", data);
            if (data.newly_unlocked && data.newly_unlocked.length > 0) {
                console.log("🔓 Unlocking items:", data.newly_unlocked);
                data.newly_unlocked.forEach(id => {
                    if (!gameState.unlockedEvidence.includes(id)) {
                        gameState.unlockedEvidence.push(id);
                    }
                });
                showNotification("🔍 NEW EVIDENCE UNLOCKED");
                
                // Wiggle DNA button
                const dnaBtn = document.getElementById('tool-dna');
                dnaBtn.classList.add('wiggle');
                
                // Append to html_content for board display
                let unlockHtml = `<div style="margin-top:5px; border-top:1px solid #ccc; padding-top:2px; font-size:0.8em; color:var(--accent-red);">🔓 NEW ITEMS UNLOCKED</div>`;
                if (data.html_content) data.html_content += unlockHtml;
                else data.description += unlockHtml; // Fallback
            }
            addEvidenceToBoard(data);
            break;
        case 'tool_error':
            showNotification("❌ " + data.message);
            break;
        case 'update_status':
            updateStatus(data);
            break;
        case 'round_failure':
            handleRoundFailure(data);
            break;
        case 'game_over':
            triggerGameOver(data);
            break;
        default:
            console.warn("Unknown action:", action);
    }
}

// --- Game Logic ---

function updateStatus(data) {
    document.getElementById('round-display').innerText = `${data.round}/3`;
    document.getElementById('points-display').innerText = data.points;
    showNotification("TIME ADVANCED (+5 PTS)");
}

function initializeGame(data) {
    gameState = data;
    
    // Fetch image metadata then render
    fetch('/static/assets/suspects/metadata.json')
        .then(res => res.json())
        .then(metadata => {
            gameState.imageMetadata = metadata;
            renderSuspects();
        })
        .catch(err => {
            console.error("Failed to load image metadata:", err);
            renderSuspects(); // Fallback
        });

    document.getElementById('loading-overlay').style.opacity = 0;
    setTimeout(() => {
        document.getElementById('loading-overlay').style.display = 'none';
    }, 1000);
    
    addChatMessage('system', `CASE LOADED: ${data.scenario.title}`);
    addChatMessage('system', `VICTIM: ${data.scenario.victim.name}`);
    
    // Update UI stats
    document.getElementById('round-display').innerText = `${data.round}/3`;
    document.getElementById('points-display').innerText = data.points;
    
    // Store Tool Data
    gameState.availableCameras = data.available_cameras || [];
    gameState.dnaMap = data.dna_map || {};
    gameState.unlockedEvidence = data.unlocked_evidence || [];
    
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

function handleRoundFailure(data) {
    showNotification("❌ " + data.message);
    
    // Update stats
    document.getElementById('round-display').innerText = `${data.round}/3`;
    document.getElementById('points-display').innerText = data.points;
    
    // Eliminate Suspect Visuals
    const card = document.querySelector(`.suspect-card[data-id="${data.eliminated_id}"]`);
    if (card) {
        card.classList.add('eliminated');
        card.onclick = null; // Disable clicking
        card.style.opacity = "0.5";
        card.style.filter = "grayscale(100%)";
        
        // Add X overlay
        const xMark = document.createElement('div');
        xMark.innerText = "❌";
        xMark.style.position = "absolute";
        xMark.style.top = "50%";
        xMark.style.left = "50%";
        xMark.style.transform = "translate(-50%, -50%)";
        xMark.style.fontSize = "5rem";
        xMark.style.color = "red";
        xMark.style.opacity = "0.8";
        card.appendChild(xMark);
    }
    
    if (gameState.currentSuspect === data.eliminated_id) {
        gameState.currentSuspect = null;
        addChatMessage('system', "Suspect eliminated. Select another.");
    }
}

function triggerGameOver(data) {
    const overlay = document.createElement('div');
    overlay.id = 'game-over-overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0,0,0,0.9)';
    overlay.style.color = 'white';
    overlay.style.display = 'flex';
    overlay.style.flexDirection = 'column';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.zIndex = '1000';
    overlay.style.fontFamily = "'Special Elite', cursive";
    
    const title = document.createElement('div');
    title.style.fontSize = '3rem';
    title.style.marginBottom = '20px';
    
    if (data.verdict) {
        title.innerText = "CASE SOLVED";
        title.style.color = "#4caf50";
    } else {
        title.innerText = "WRONG ACCUSATION";
        title.style.color = "#f44336";
    }
    
    const msg = document.createElement('div');
    msg.innerText = data.message;
    msg.style.fontSize = '1.5rem';
    msg.style.maxWidth = '600px';
    msg.style.textAlign = 'center';
    msg.style.marginBottom = '40px';
    
    const btn = document.createElement('button');
    btn.innerText = "PLAY AGAIN";
    btn.className = "modal-btn confirm";
    btn.style.fontSize = "1.5rem";
    btn.onclick = () => location.reload();
    
    overlay.appendChild(title);
    overlay.appendChild(msg);
    overlay.appendChild(btn);
    
    document.body.appendChild(overlay);
}

// --- UI Rendering: Suspects ---

function renderSuspects() {
    const container = document.getElementById('suspect-files');
    container.innerHTML = '<div class="folder-label">SUSPECTS</div>';
    
    if (!gameState.scenario || !gameState.scenario.suspects) return;

    gameState.scenario.suspects.forEach((suspect, index) => {
        const card = document.createElement('div');
        card.className = 'suspect-card';
        card.dataset.id = suspect.id;
        card.onclick = () => selectSuspect(suspect.id);
        
        // Placeholder Avatar (Initials)
        const initials = suspect.name.split(' ').map(n => n[0]).join('');
        
        // Select Image based on Gender & Archetype
        let imgFilename = `suspect_${(index % 8) + 1}.jpg`; // Default fallback
        
        if (gameState.imageMetadata && gameState.imageMetadata.length > 0 && suspect.gender) {
            // 1. Filter by Gender
            const genderMatches = gameState.imageMetadata.filter(img => img.gender === suspect.gender.toLowerCase());
            
            if (genderMatches.length > 0) {
                // 2. Try to match Archetype
                const role = suspect.role.toLowerCase();
                let targetArchetype = "detective"; // default
                
                if (role.includes("ceo") || role.includes("cfo") || role.includes("manager") || role.includes("dealer")) targetArchetype = "executive";
                else if (role.includes("janitor") || role.includes("chef") || role.includes("caterer")) targetArchetype = "worker";
                else if (role.includes("artist") || role.includes("curator")) targetArchetype = "artist";
                else if (role.includes("heir") || role.includes("collector") || role.includes("sister") || role.includes("socialite")) targetArchetype = "socialite";
                else if (role.includes("ex-")) targetArchetype = "criminal";
                else if (role.includes("customer")) targetArchetype = "customer"; // Rough/casual look
                
                const archetypeMatches = genderMatches.filter(img => img.archetype === targetArchetype);
                
                // Use archetype matches if available, otherwise use all gender matches
                const pool = archetypeMatches.length > 0 ? archetypeMatches : genderMatches;
                
                // Deterministic pick based on name
                let hash = 0;
                for (let i = 0; i < suspect.name.length; i++) {
                    hash = ((hash << 5) - hash) + suspect.name.charCodeAt(i);
                    hash |= 0; 
                }
                const selected = pool[Math.abs(hash) % pool.length];
                imgFilename = selected.id;
            }
        }
        
        card.innerHTML = `
            <div class="suspect-img">
                <img src="/static/assets/suspects/${imgFilename}" 
                     style="width:100%; height:100%; object-fit:cover; display:block;" 
                     onerror="this.style.display='none'; this.parentElement.innerText='${initials}'; this.parentElement.style.display='flex'; this.parentElement.style.alignItems='center'; this.parentElement.style.justifyContent='center';">
            </div>
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
    
    const displayName = name ? name.toUpperCase() : role.toUpperCase();
    
    // Immediate render for user/system
    if (role !== 'suspect' && role !== 'assistant') {
        msg.innerHTML = `<strong>${displayName}:</strong> ${text}`;
        log.appendChild(msg);
        log.scrollTop = log.scrollHeight;
        return;
    }

    // Typing effect for suspects
    msg.innerHTML = `<strong>${displayName}:</strong> <span class="typing-text"></span>`;
    log.appendChild(msg);
    
    const span = msg.querySelector('.typing-text');
    let i = 0;
    const speed = 20; // ms per char
    
    function type() {
        if (i < text.length) {
            span.textContent += text.charAt(i);
            i++;
            log.scrollTop = log.scrollHeight; // Auto-scroll
            setTimeout(type, speed);
        }
    }
    
    type();
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
    const optionsContainer = document.getElementById('modal-options');
    const promptText = document.getElementById('modal-prompt-text');
    
    const section2 = document.getElementById('modal-section-2');
    const input2 = document.getElementById('modal-input-2');
    const promptText2 = document.getElementById('modal-prompt-text-2');
    
    // Reset
    section2.style.display = 'none';
    input.style.display = 'block';
    optionsContainer.style.display = 'none';
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
        promptText.innerText = "Select Evidence to Test:";
        
        // Stop wiggling if clicked
        document.getElementById('tool-dna').classList.remove('wiggle');
        
        if (gameState.unlockedEvidence.length === 0) {
            showNotification("⚠️ No physical evidence found yet. Check camera footage!");
            return; 
        }
        input.style.display = 'none';
        populateOptionList(gameState.unlockedEvidence, gameState.dnaMap);
    } else if (toolName === 'get_footage') {
        promptText.innerText = "Select Camera Feed:";
        input.style.display = 'none';
        populateOptionList(gameState.availableCameras);
    } else if (toolName === 'accuse') {
        // ... existing accuse logic ...
        if (!gameState.currentSuspect) {
            showNotification("⚠️ Select a suspect to accuse!");
            closeModal();
            return;
        }
        const suspect = gameState.scenario.suspects.find(s => s.id === gameState.currentSuspect);
        promptText.innerText = `ACCUSE ${suspect.name.toUpperCase()}?`;
        input.placeholder = "Type 'GUILTY' to confirm";
    }
    
    modal.classList.add('active');
    if (input.style.display !== 'none') input.focus();
}

function populateOptionList(items, labelMap = null) {
    const container = document.getElementById('modal-options');
    container.innerHTML = '';
    container.style.display = 'flex';
    
    items.forEach((item, index) => {
        const wrapper = document.createElement('div');
        wrapper.className = 'modal-option-item';
        wrapper.onclick = () => {
            wrapper.querySelector('input').checked = true;
        };
        
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'tool-option';
        radio.value = item;
        radio.id = `opt-${index}`;
        if (index === 0) radio.checked = true;
        
        const label = document.createElement('label');
        label.htmlFor = `opt-${index}`;
        
        let text = item;
        if (labelMap && labelMap[item]) {
            text = labelMap[item];
        } else {
            text = item.replace(/_/g, ' ').toUpperCase();
        }
        label.innerText = text;
        
        wrapper.appendChild(radio);
        wrapper.appendChild(label);
        container.appendChild(wrapper);
    });
}

function submitTool() {
    const input = document.getElementById('modal-input');
    const optionsContainer = document.getElementById('modal-options');
    
    let value = input.value.trim();
    
    // Use radio value if visible
    if (optionsContainer.style.display !== 'none') {
        const selected = optionsContainer.querySelector('input[name="tool-option"]:checked');
        if (selected) {
            value = selected.value;
        } else {
            value = '';
        }
    }
    
    const confirmBtn = document.getElementById('modal-confirm');
    
    if (!pendingTool) return;
    
    let payload = null;
    // ... rest of submitTool ... (Logic remains same as it uses 'value')
    
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
    } else if (pendingTool === 'accuse') {
         if (value.toUpperCase() === 'GUILTY') {
            payload = { 
                tool: 'accuse', 
                suspect_id: gameState.currentSuspect 
            };
        } else {
            showModalError("Type 'GUILTY' to confirm accusation.");
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
            } else if (result && result.action === 'add_evidence') {
                // Success: Show result in modal
                showModalResult(result.data);
                // Auto-close after 5s
                setTimeout(closeModal, 5000);
            } else {
                closeModal();
            }
        });
    }
}

function showModalResult(data) {
    // Hide inputs
    document.getElementById('modal-input').style.display = 'none';
    document.getElementById('modal-options').style.display = 'none';
    document.getElementById('modal-section-2').style.display = 'none';
    document.getElementById('modal-prompt-text').style.display = 'none';
    
    // Show result
    let resultDiv = document.getElementById('modal-result');
    if (!resultDiv) {
        resultDiv = document.createElement('div');
        resultDiv.id = 'modal-result';
        resultDiv.style.marginTop = '20px';
        resultDiv.style.borderTop = '2px dashed var(--ink-color)';
        resultDiv.style.paddingTop = '10px';
        document.querySelector('.modal-content').insertBefore(resultDiv, document.querySelector('.modal-actions'));
    }
    
    resultDiv.style.display = 'block';
    
    let html = `
        <div style="font-weight:bold; margin-bottom:5px;">RESULT:</div>
        ${data.html_content || data.description}
    `;
    
    if (data.newly_unlocked && data.newly_unlocked.length > 0) {
        html += `<div class="unlocked-list"><strong>🔓 UNLOCKED FOR DNA TEST:</strong><ul>`;
        data.newly_unlocked.forEach(id => {
            let label = id;
            if (gameState.dnaMap && gameState.dnaMap[id]) {
                label = gameState.dnaMap[id];
            }
            html += `<li>${label}</li>`;
        });
        html += `</ul></div>`;
    }
    
    resultDiv.innerHTML = html;
    
    // Change button
    const btn = document.getElementById('modal-confirm');
    btn.innerText = "CLOSE";
    btn.onclick = closeModal;
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
    
    const resultDiv = document.getElementById('modal-result');
    if (resultDiv) resultDiv.style.display = 'none';
    
    const btn = document.getElementById('modal-confirm');
    btn.innerText = "SUBMIT";
    btn.onclick = submitTool;
    btn.disabled = false;
    
    // Reset inputs visibility for next time (useTool will override, but safe default)
    document.getElementById('modal-input').style.display = 'block';
    document.getElementById('modal-prompt-text').style.display = 'block';
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
document.getElementById('tool-accuse').onclick = () => useTool('accuse');

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
