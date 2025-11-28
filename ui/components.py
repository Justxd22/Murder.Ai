def format_tool_result_markdown(tool_name, result):
    """Formats tool output as Markdown for the chat interface and evidence board."""
    if "error" in result:
        return f"❌ **Error:** {result['error']}"

    output = ""
    if tool_name == "get_location":
        output += "### 📍 Location Data\n"
        if "history" in result:
            output += "**Movement History:**\n"
            for h in result['history']:
                # Try to make history lines cleaner if they are just strings
                output += f"- {h}\n"
        elif "info" in result and result['info'] != "Location History Found": 
             # Only show info if it's an error or specific status, skip generic "Found"
            output += f"**Status:** {result['info']}\n\n"

    elif tool_name == "get_footage":
        output += f"### 📹 CCTV Analysis\n"
        output += f"- **Location:** {result.get('location', 'Unknown')}\n"
        output += f"- **Time:** {result.get('time_range', 'N/A')}\n"
        output += f"- **Quality:** {result.get('quality', 'N/A')}\n"
        if "visible_people" in result:
            people = ", ".join(result['visible_people'])
            output += f"- **Visible:** {people}\n"
        if "key_details" in result:
            output += f"- **Key Details:** {result['key_details']}\n"

    elif tool_name == "get_dna_test":
        output += "### 🧬 DNA Analysis\n"
        output += f"**Sample ID:** {result.get('evidence_id', 'Unknown')}\n"
        if "result" in result:
            output += f"**Result:** {result['result']}\n"
        if "match" in result: 
            output += f"**Match:** {result['match']}\n"

    elif tool_name == "call_alibi":
        output += "### 📞 Alibi Check\n"
        if "status" in result: 
            output += f"**Status:** {result['status']}\n"
        if "statement" in result: 
            output += f"**Statement:** \"{result['statement']}\"\n"
    
    else:
        # Fallback for unknown tools or simple strings
        output = str(result)
    
    return output

def format_suspect_card(suspect):
    """Generates HTML for a suspect card."""
    return f"""
    <div class="suspect-card">
        <h3>{suspect['name']}</h3>
        <p><strong>Role:</strong> {suspect['role']}</p>
        <p><strong>Bio:</strong> {suspect['bio']}</p>
        <p><strong>Phone:</strong> {suspect.get('phone_number', 'N/A')}</p>
        <div style="margin-top: 5px; font-size: 0.8em; color: #666;">ID: {suspect['id']}</div>
    </div>
    """
