import React, { useEffect, useState } from 'react';
import Spinner from '../Spinner';
import NotFound from '../NotFound';
import GenericError from '../GenericError';
import CertificatePreview from '../CertificatePreview';
import { fetchCertificateData } from '../../utils';

const App = () => {
	const [isLoading, setIsLoading] = useState(true);
	const [isNotFound, setIsNotFound] = useState(false);
	const [isGenericError, setIsGenericError] = useState(false);
	const [certificateData, setCertificateData] = useState({});

	useEffect(() => {
		fetchCertificateData()
			.then((response) => {
				setIsLoading(false);
				setCertificateData(response);
			})
			.catch((error) => {
				if (error && error.status === 404) setIsNotFound(true);
				else setIsGenericError(true);

				setIsLoading(false);
			});
	}, []);

	const renderContent = () => {
		const isCertificateData = !!Object.keys(certificateData).length;

		if (isLoading) return <Spinner />;

		if (isNotFound) return <NotFound />;

		if (isGenericError) return <GenericError />;

		if (isCertificateData) return <CertificatePreview certificateData={certificateData} />;

		return false;
	};

	return (
		<div>
			{renderContent()}
		</div>
	);
};

export default App;
