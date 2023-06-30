CREATE DATABASE "main";
\c "main";

CREATE TABLE "product" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    PRIMARY KEY ("id")
);

CREATE TABLE "product_version" (
    "id" SERIAL NOT NULL,
    "version" VARCHAR(10) NOT NULL,
    "product_id" INTEGER NOT NULL,
    PRIMARY KEY ("id"),
    CONSTRAINT product_fk FOREIGN KEY(product_id) REFERENCES "product"(id)
);

CREATE TABLE "ticket" (
    "id" SERIAL NOT NULL,
    "title" VARCHAR(100) NOT NULL,
    "description" VARCHAR(1000) NOT NULL,
    "state" INTEGER NOT NULL,
    "SLA" TIMESTAMP NOT NULL,
    "priority" INTEGER NOT NULL,
    "severity" INTEGER NOT NULL,
    "product_version_id" INTEGER NOT NULL,
    "resource_name" VARCHAR(100),
    "client_id" INTEGER NOT NULL,
    "created_date" TIMESTAMP NOT NULL,
    "updated_date" TIMESTAMP NOT NULL,
    PRIMARY KEY ("id"),
    CONSTRAINT product_version_fk FOREIGN KEY(product_version_id) REFERENCES "product_version"(id)
);

CREATE TABLE "task" (
    "ticket_id" INTEGER NOT NULL,
    "task_id" INTEGER NOT NULL, 
    PRIMARY KEY ("ticket_id", "task_id"),
    CONSTRAINT ticket_fk FOREIGN KEY(ticket_id) REFERENCES "ticket"(id)
);