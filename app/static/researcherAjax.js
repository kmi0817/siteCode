$(document).ready(() => {
    // 페이지 로드 시 세션에 있는 초대장 값 가져와 화면에 출력
    sessionStorage.getItem("invitation");
    var invitation = sessionStorage.getItem("temp");
    $(".showInfo").html(invitation);

    $("#acceptInvitation").click(() => {
        $.ajax({
            type: "POST",
            url: "http://localhost:8031/connections/receive-invitation",
            data: invitation,
            datatype: "json"
        })
            .always((res) => {
                var appended = `
                <div class="div">
                    <div class="label">DID</div>
                    <pre class="showInfo">did.. sample</pre>
                </div>
                <div class="div">
                    <div class="label">Credentials</div>
                </div>
                `;
                $("#container").append(appended);
            })
    })
})