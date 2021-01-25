import React, { useRef } from 'react';
import PropTypes from 'prop-types';
import domtoimage from 'dom-to-image';
import logo from './academia_blockchain_logo.png';
import './index.sass';

const CertificatePreview = ({ certificateData }) => {
	const certificateNode = useRef(null);
	const styleFlexCenterColumn = 'd-flex justify-content-center align-items-center flex-column';
	const handleDownload = (ref) => {
		domtoimage.toJpeg(ref.current)
			.then((dataUrl) => {
				const link = document.createElement('a');
				link.download = 'CERTIFICADO_ACBC.jpeg';
				link.href = dataUrl;
				link.click();
			});
	};

	return (
		<div className={styleFlexCenterColumn}>
			<div ref={certificateNode} aria-label="Vista previa del certificado" className="w-100">
				<div className="certificate__border">
					<div className="certificate__container">
						<header className="certificate__header p-1">
							<div className="certificate__logo-container">
								<img alt="ACBC Logo" src={logo} />
							</div>
							<div className="certificate__acbc-title text-center">Certificación de Academia Blockchain</div>
							<div className="certificate__date">{certificateData.date}</div>
						</header>
						<main className={styleFlexCenterColumn}>
							<div className="certificate__graduate">{certificateData.graduate}</div>
							<div className="certificate__pre-title text-center">ha completado exitosamente la certificación en</div>
							<div className="certificate__title">{certificateData.title}</div>
							<div className="certificate__author">{certificateData.author}</div>
							<div className="certificate__description text-center">{certificateData.description}</div>
						</main>
						<footer className={styleFlexCenterColumn}>
							<div className="certificate__footer text-break mt-3">
								Id de la transaction:
							</div>
							<div className="certificate__footer text-break text-center">{certificateData.txId}</div>
						</footer>
					</div>
				</div>
			</div>

			<div className="m-3">
				<a
					href={`https://etherscan.io/tx/${certificateData.txId}`}
					target="_blank"
					rel="noreferrer"
				>
					Ver transacción en la blockchain
				</a>
			</div>
			<div className="m-3">
				<button onClick={() => handleDownload(certificateNode)} type="button" className="btn btn-primary">
					DESCARGAR
				</button>
			</div>
		</div>
	);
};

CertificatePreview.propTypes = {
	certificateData: PropTypes.shape({
		graduate: PropTypes.string.isRequired,
		title: PropTypes.string.isRequired,
		author: PropTypes.string.isRequired,
		date: PropTypes.string.isRequired,
		description: PropTypes.string.isRequired,
		txId: PropTypes.string.isRequired
	}).isRequired
};

export default CertificatePreview;
