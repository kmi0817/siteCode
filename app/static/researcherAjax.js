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
                var schema_ids = sessionStorage.getItem("schema_ids"); // 세션에서 스키마ID 가져오기
                schema_ids = schema_ids.split(","); // 스키마ID 배열로 만들기 (string -> array)
                var schema_ids_tag = ""; // 스키마ID 라디오 버튼 담을 태그
                // 스키마ID 라디오 버튼 생성하여 태그에 추가
                schema_ids.forEach((id) => {
                    schema_ids_tag += `
                        <label>
                            <input type="radio" name="schema_ids" value="${id}">${id}
                        </label>
                        <br>
                        `;
                })

                // 추가할 태그 1) DID 2) 스키마ID 라디오 버튼 3) 스키마
                var appended = `
                <div class="div">
                    <div class="label">DID</div>
                    <div class="showInfo">${res["my_did"]}</div>
                </div>
                <div class="div">
                    <div class="label">schemaID</div>
                    <div class="showInfo">${schema_ids_tag}</div>
                    <input type="button" id="selectSchemaId" class="btns" value="credential 선택">
                </div>
                <div class="div">
                    <div class="label">스키마</div>
                    <div id="displaySchema" class="showInfo"></div>
                </div>
                `;
                $("#container").append(appended);
            });
    });

    $(document).on("click", "#selectSchemaId", () => {
        var selectedId = $("input:radio[name=schema_ids]:checked").val();
        if (selectedId) {
            var schema = sessionStorage.getItem(selectedId);
            console.log(schema);
            if (schema) {
                $("#displaySchema").html(schema);
            } else {
                alert("해당 스키마ID에 속하는 스키마가 없습니다.");
            }
        } else {
            alert("스미카ID를 선택하세요.");
        }
    });
})