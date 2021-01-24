import React from 'react';

const GenericError = () => (
	<div>
		<div className="text-center p-3 text-danger">Ha ocurrido un error</div>
		<div className="text-center p-3">Por favor intente más tarde</div>
		<div className="text-center p-3">
			<a href="/">Regresar al inicio</a>
		</div>
		<div className="glyphicon glyphicon-remove" />
	</div>
);

export default GenericError;
