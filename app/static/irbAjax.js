$(document).ready(() => {
    // IRB 페이지 로드 시 바로 초대장 생성
    $.ajax({
        type: "POST",
        url: "http://localhost:8021/connections/create-invitation"
    })
        .done((res) => {
            var invitation = JSON.stringify(res.invitation); // 초대장 받기
            sessionStorage.setItem("invitation", invitation); // 초대장 세션 등록
        })
        .always(() => {
            sessionStorage.setItem("temp", "[{'invitation': 'hi'}, {'user' : 'kmi'}]");
        })
})