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

// eslint-disable-next-line no-unused-vars
const mockedNotFoundResponse = {
	success: false,
	status: 404
};

// eslint-disable-next-line no-unused-vars
const mockedErrorResponse = {
	success: false,
	status: 500
};

// eslint-disable-next-line import/prefer-default-export
export const fetchCertificateData = () => new Promise((resolve) => {
	setTimeout(() => resolve(mockedCertificateData), 900);
});
