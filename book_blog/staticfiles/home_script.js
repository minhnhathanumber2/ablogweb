function starHover(num){
    for (let i = 1; i<=5; ++i) document.getElementById("star_" + i).classList.remove("rated");
    for (let i = 1; i<=num; ++i) document.getElementById("star_" + i).classList.add("rated");
}
function generateParagraph(){
    let paragraphs = document.getElementsByClassName("paragraph").length;
    document.getElementById("paragraph_area").insertAdjacentHTML("beforeend",  `
        <div class="paragraph">
            <h3>Đoạn ` + (paragraphs + 1) + `:</h3>
            <h4>Tiêu đề ` + (paragraphs + 1) + `:</h4>
            <input type="text" name="paragraph-title" maxlength="100" required id="id_paragraph-title" placeholder="Tiêu đề">
            <h4>Nội dung ` + (paragraphs + 1) + `<span style="color: red;" title="Thẻ này có thể áp dụng Markdown.">*</span>:</h4>
            <textarea name="paragraph-detail" cols="40" rows="10" required id="id_paragraph-detail" placeholder="Nội dung"></textarea>
        </div>
    `);
}

function deleteParagraph(){
    let paragraphs = document.getElementsByClassName("paragraph")
    if (paragraphs.length > 0) paragraphs[paragraphs.length - 1].remove();
}

