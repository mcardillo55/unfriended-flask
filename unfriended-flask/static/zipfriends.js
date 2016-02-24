var zip = new JSZip();
function zipHTML(){
    htmlFile = $('input[type=file]').get(0).files[0];
    //console.log($('input[type=file]').get(0).files[0]);
    fr = new FileReader();
    fr.onload = loadedText;
    fr.readAsText(htmlFile);

    function loadedText() {
        zip.file("fbHTML.html", fr.result);
        zippedFile = zip.generate({type:"base64", compression:"DEFLATE"});

        $('input[type=hidden]').val(zippedFile);
        $('#zipped').submit();
    }

    /*$.ajax({
                url: '/',
               type: 'POST',
        contentType: 'application/octet-stream',  
               data: zippedFile,
        processData: false
})*/
}
//zip.file()