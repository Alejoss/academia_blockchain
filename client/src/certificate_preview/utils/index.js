const mockedCertificateData = {
	graduate: 'Esteban el Estudiante',
	title: 'Curso de Cosas',
	author: 'Profesor Juan Pérez',
	date: 'Jan-05-2021 07:44:21 PM + UTC',
	description: 'Este curso consiste en aprender cosas.',
	txId: '0xbed43af4d271362da3b85a370f9226fcde9e78c2c98e2bfd74d6774c2261a3fa'
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
