import React from 'react';

const NotFound = () => (
	<div>
		<div className="text-center p-3 font-weight-bold">ERROR 404</div>
		<div className="text-center p-3 text-danger">No pudimos encontrar los datos de este certificado</div>
		<div className="text-center p-3">
			<a href="/">Regresar al inicio</a>
		</div>
		<div className="glyphicon glyphicon-remove" />
	</div>
);

export default NotFound;
