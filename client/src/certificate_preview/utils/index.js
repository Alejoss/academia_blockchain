// eslint-disable-next-line no-unused-vars
const mockedCertificateData = {
	"id": '0xbed43af4d271362da3b85a370f9226fcde9e78c2c98e2bfd74d6774c2261a3fa',
	"username": 'Juan Tarufetti',
	"first_name": 'Juan',
	"last_name": 'Tarufetti',
	"cert_date": 'Jan-05-2021 07:44:21 PM + UTC',
	"event_title": 'Curso de Plomería',
	"event_description": 'Este curso consiste en aprender cuestiones básicas de plomería.',
	"event_owner_username": 'Licenciado Juan Varela',
	"event_owner_first_name": 'Licenciado Juan',
	"event_owner_last_name": 'Varela',
};

export const fetchCertificateData = certificate_id => new Promise((resolve, reject) => {
	const certificate_details_url = `/courses/certificate_detail/${certificate_id}`;

	fetch(certificate_details_url)
		.then(response => {
			if (response.status === 200) return response.json();
			else reject({ status: response.status });
		})
		.then(resolve)
		.catch(reason => {
			console.error('TESTSSSS', reason); // eslint-disable-line no-console
			reject({ status: 123456 });
		})
	});

export const getCertificateIdFromUrl = () => window.location.href.split('certificate_preview/')[1];
