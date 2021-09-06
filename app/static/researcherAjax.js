$(document).ready(() => {
    // 페이지 로드 시 세션에 있는 초대장 값 가져와 화면에 출력
    var invitation = sessionStorage.getItem("invitation");
    // var invitation = sessionStorage.getItem("temp");
    $(".showInfo").text(invitation);

    $("#acceptInvFromIrb").click(() => {
        $.ajax({
            type: "POST",
            url: "http://localhost:8031/connections/receive-invitation",
            data: invitation,
            datatype: "json"
        })
            .done((res) => {
                var cred_def_ids = sessionStorage.getItem("credential_definition_ids"); // 세션에서 스키마ID 가져오기
                cred_def_ids = cred_def_ids.split(","); // 스키마ID 배열로 만들기 (string -> array)
                var cred_def_ids_tag = ""; // 스키마ID 라디오 버튼 담을 태그
                // 스키마ID 라디오 버튼 생성하여 태그에 추가
                cred_def_ids.forEach((id) => {
                    cred_def_ids_tag += `
                        <label>
                            <input type="radio" name="cred_def_ids" value="${id}">${id}
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
                    <div class="label">cred def ID</div>
                    <div class="showInfo">${cred_def_ids_tag}</div>
                    <input type="button" id="selectCreddefId" class="btns" value="credential 선택">
                </div>
                <div class="div">
                    <div class="label">Cred def</div>
                    <div id="displayCreddef" class="showInfo"></div>
                </div>
                `;
                $("#container_irb").append(appended);
            });
    });

    $(document).on("click", "#selectCreddefId", () => {
        var selectedId = $("input:radio[name=cred_def_ids]:checked").val();
        if (selectedId) {
            var creddef = sessionStorage.getItem(selectedId);
            if (creddef) {
                $("#displayCreddef").html(creddef);
            } else {
                alert("해당 ID에 속하는 credential definition이 없습니다.");
            }
        } else {
            alert("credential definition ID를 선택하세요.");
        }
    });
})