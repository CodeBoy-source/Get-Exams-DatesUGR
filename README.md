# Get-Exams-DatesUGR
Esta aplicación realiza una búsqueda de los últimos 'pdfs' de publicados
por la _Escuela Técnica y Superior de Ingenierías Informáticas y de Telecomunicación_
respecto a las fechas y horarios de los exámenes de todos los grados
relacionados.

Una vez obtenido los 'pfds' utiliza modelos de interpretado para poder
generar, tras una limpieza y pre-procesado, un conjunto de archivos `.csv`
separados para cada grado.

Por último los une en uno entero denominado `merged.csv`.

Además, para el uso de esta información para otra práctica se almacenó
nombre y siglas de los exámenes. Todo se guarda en `datos/`
