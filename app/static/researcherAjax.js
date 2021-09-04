$(document).ready(() => {
    // 페이지 로드 시 세션에 있는 초대장 값 가져와 화면에 출력
    var invitation = sessionStorage.getItem("invitation");
    // var invitation = sessionStorage.getItem("temp");
    $(".showInfo").text(invitation);

    $("#acceptInvitation").click(() => {
        $.ajax({
            type: "POST",
            url: "http://localhost:8031/connections/receive-invitation",
            data: invitation,
            datatype: "json"
        })
            .done((res) => {
                // console.log(res);
                var schema_ids = sessionStorage.getItem("schema_ids");
                schema_ids = schema_ids.split(",");
                var schema_ids_tag = "<form>";
                schema_ids.forEach((id) => {
                    schema_ids_tag += `
                        <label>
                            <input type="radio" name="schema_ids">${id}</input><br>
                        </label>
                        `;
                })
                schema_ids_tag += "</form>";

                console.log(schema_ids_tag);
                var appended = `
                <div class="div">
                    <div class="label">DID</div>
                    <div class="showInfo">${res["my_did"]}</div>
                </div>
                <div class="div">
                    <div class="label">schemas</div>
                    <div class="showInfo">${schema_ids_tag}</div>
                </div>
                `;
                $("#container").append(appended);
            });
    })
})