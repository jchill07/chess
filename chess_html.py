
def setup_tournament():
    return '''
        <div id = "header">
            <h1>Setup A New Tournament</h1>
        </div>
        <div id="debug_div"></div>
		
        <div id="body_div"> <table>
            <tr>
                <th><label id="t_name">Tournament Name:</label></th>
                <td><input id="tournamt_name" type="text"/></td>
            </tr>
            <tr>
                <th><label id="t_date">Tournament Date (YYYYMMDD):</label></th>
                <td><input id="tournamt_date" type="text"/></td>
            </tr>
            <tr>
                <th><label id="t_r_code">Root Code:</label></th>
                <td><input id="root_code1" type="text"/></td>
                <td><input id="root_code2" type="text"/></td>
            </tr>
            <tr>
                <th><label id="t_v_code">View Code:</label></th>
                <td><input id="view_code1" type="text"/></td>
                <td><input id="view_code2" type="text"/></td>
            </tr>
            <tr>
                <td>
                    <button id="match_code_submit" type="button" onclick="check_tournament();">
                        Submit
                    </button>
                </td>
            </tr>
        </div></table>
        <div id = "footer">
            <script>
                var match_text_box = document.getElementById("match_code");
                match_text_box.addEventListener("keydown", function (e) {
                    if (e.key === "Enter") {
                        check_match_code();
                    }
                });
            </script>
        </div>
        

    '''
