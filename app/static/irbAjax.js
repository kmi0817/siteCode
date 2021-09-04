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
                    var schema_ids = res["schema_ids"];
                    schema_ids.push("testSChemas");
                    console.log(schema_ids);
                    sessionStorage.setItem("schema_ids", schema_ids)
                });
        });

    $("#logout").click(() => {
        if (sessionStorage.getItem("connection_id")) {
            var connection_id = sessionStorage.getItem("connection_id");
            $.ajax({
                type: "DELETE",
                url: `http://localhost:8021/connections/${connection_id}`
            })
                .done((res) => {
                    console.log("connection deleted")
                });
        }
    })
})