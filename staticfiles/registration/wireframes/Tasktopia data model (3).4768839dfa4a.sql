CREATE TABLE "users" (
  "user_id" integer PRIMARY KEY,
  "username" varchar(50),
  "password" varchar(50),
  "email" varchar(225),
  "first_name" varchar(225),
  "last_name" varchar(225),
  "date_joined" timestamp,
  "last_login" timestamp,
  "is_active" bool,
  "is_staff" bool,
  "is_superuser" bool
);

CREATE TABLE "categories" (
  "category_id" integer PRIMARY KEY,
  "category" varchar(225),
  "created_at" timestamp,
  "user_id" integer,
  "task_id" integer
);

CREATE TABLE "tasks" (
  "task_id" integer PRIMARY KEY,
  "title" varchar,
  "description" text,
  "due_date" timestamp,
  "priority" varchar,
  "status" varchar,
  "created_at" timestamp,
  "updated_at" timestamp,
  "category_id" integer
);

COMMENT ON COLUMN "categories"."user_id" IS 'foreign key to users table Foriegn key to services table (One to many (one user, many categories)';

COMMENT ON COLUMN "categories"."task_id" IS 'foreign key to users table Foriegn key to services table (One to many (one user, many categories)';

COMMENT ON COLUMN "tasks"."description" IS 'Content of the task';

COMMENT ON COLUMN "tasks"."category_id" IS 'foreign key to Categories table';

ALTER TABLE "categories" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

ALTER TABLE "categories" ADD FOREIGN KEY ("task_id") REFERENCES "tasks" ("task_id");

ALTER TABLE "tasks" ADD FOREIGN KEY ("category_id") REFERENCES "users" ("user_id");
