import domtoimage from 'dom-to-image';
import './index.sass';

const certificateNode = document.getElementById('certificate__wrapper');
const buttonDownloadCertificate = document.getElementById('button-print-certificate');
const errorMessageNode = document.getElementById('error-message');
const errorMessage = 'ERROR';

const downloadCertificate = () => {
    domtoimage.toJpeg(certificateNode)
        .then(function (dataUrl) {
            var link = document.createElement('a');
            link.download = 'CERTIFICADO_ACBC.jpeg';
            link.href = dataUrl;
            link.click();
        });
};

if (buttonDownloadCertificate && certificateNode && domtoimage) {
    buttonDownloadCertificate.addEventListener('click', downloadCertificate);
} else if (errorMessageNode) {
    errorMessageNode.innerHTML = errorMessage;
}
