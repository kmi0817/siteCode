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
                url: "http://localhost:8021/schemas/created",
            })
                .done((res) => {
                    var schema_ids = res["schema_ids"]; // 스키마ID 배열로 반환
                    sessionStorage.setItem("schema_ids", schema_ids); // 스키마ID 세션 등록

                    // 반환받은 모든 스키마ID의 스키마를 세선에 등록함
                    schema_ids.forEach((id) => {
                        $.ajax({
                            type: "GET",
                            url: `http://localhost:8021/schemas/${id}`
                        })
                            .done((res) => {
                                // 스키마ID에 해당하는 스키마 세션 등록
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