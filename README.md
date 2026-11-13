# Laboratorio 11 - Terraform y Floci



## Descripción

Infraestructura Big Data como Código utilizando Terraform y Floci para emular servicios AWS localmente.



Curso: Business Intelligence and Big Data

Universidad: Universidad César Vallejo



## Tecnologías

- Terraform

- Docker Desktop

- Floci

- AWS CLI

- Git/GitHub



## Infraestructura

- 1 bucket S3: ucv-data-platform

- 4 dominios: sales, customers, products y marketing

- 3 capas: bronze, silver y gold

- 4 bases de datos AWS Glue Data Catalog



## Ejecución

1. docker compose up -d

2. cd terraform

3. terraform init

4. terraform validate

5. terraform plan

6. terraform apply



## Verificación

- aws --endpoint-url http://localhost:4566 s3 ls

- aws --endpoint-url http://localhost:4566 glue get-databases



## Seguridad

Los archivos terraform.tfstate, la carpeta .terraform y los datos locales están excluidos de Git.



## Observación

Se utiliza ignore_changes para las etiquetas de Glue debido a diferencias de compatibilidad con Floci.


