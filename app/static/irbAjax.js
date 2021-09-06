$(document).ready(() => {
    // IRB 페이지 로드 시 바로 초대장 생성
    $.ajax({
        type: "POST",
        url: "http://localhost:8021/connections/create-invitation"
    })
        .done((res) => {
            var invitation = JSON.stringify(res.invitation); // 초대장 받기
            sessionStorage.setItem("invitation", invitation); // 초대장 세션 등록

            $.ajax({
                type: "GET",
                url: "http://localhost:8021/credential-definitions/created",
            })
                .done((res) => {
                    var creddef_ids = res["credential_definition_ids"]; // cred def ID 배열로 반환
                    sessionStorage.setItem("credential_definition_ids", creddef_ids); // cred def ID 세션 등록

                    // 반환받은 모든 cred def ID의 cred def를 세선에 등록함
                    creddef_ids.forEach((id) => {
                        $.ajax({
                            type: "GET",
                            url: `http://localhost:8021/credential-definitions/${id}`
                        })
                            .done((res) => {
                                // cred def ID에 해당하는 cred def 세션 등록
                                sessionStorage.setItem(id, JSON.stringify(res));
                            })
                    });
                });
        });

    $("#logout").click(() => { // 이거 안 먹힘..
        if (sessionStorage.getItem("connection_id")) {
            var connection_id = sessionStorage.getItem("connection_id");
            $.ajax({
                type: "DELETE",
                url: `http://localhost:8021/connections/${connection_id}`
            })
                .done((res) => {
                    alert("connection deleted");
                    sessionStorage.clear();
                });
        }
    })
})