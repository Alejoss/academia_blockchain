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
							<div className="certificate__date">{certificateData.cert_date}</div>
						</header>
						<main className={styleFlexCenterColumn}>
							<div className="certificate__username">{certificateData.username}</div>
							<div className="certificate__pre-title text-center">ha completado exitosamente la certificación en</div>
							<div className="certificate__title">{certificateData.event_title}</div>
							<div className="certificate__author text-center">Dictado por: {certificateData.event_owner_username}</div>
							<div className="certificate__description text-center">{certificateData.event_description}</div>
						</main>
						<footer className={styleFlexCenterColumn}>
							<div className="certificate__footer text-break mt-3">
								Este certificado todavía no figura en la blockchain
							</div>
						</footer>
					</div>
				</div>
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
		id: PropTypes.number.isRequired,
		username: PropTypes.string.isRequired,
		first_name: PropTypes.string.isRequired,
		last_name: PropTypes.string.isRequired,
		cert_date: PropTypes.string.isRequired,
		event_title: PropTypes.string.isRequired,
		event_description: PropTypes.string.isRequired,
		event_owner_username: PropTypes.string.isRequired,
		event_owner_first_name: PropTypes.string.isRequired,
		event_owner_last_name: PropTypes.string.isRequired,
	}).isRequired
};

export default CertificatePreview;
