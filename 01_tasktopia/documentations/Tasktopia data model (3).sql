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
  "category_id" integer,
  "user_id" integer
);

CREATE TABLE "notifications" (
  "notification_id" integer PRIMARY KEY,
  "message" text,
  "sent_at" timestamp,
  "user_id" integer,
  "task_id" integer
);

CREATE TABLE "reports" (
  "report_id" integer PRIMARY KEY,
  "generated_at" timestamp,
  "content" text,
  "user_id" integer
);

CREATE TABLE "weather" (
  "weather_id" integer PRIMARY KEY,
  "current_date" timestamp,
  "projected_day_2" timestamp,
  "projected_day_3" timestamp,
  "projected_day_4" timestamp,
  "projected_day_5" timestamp,
  "condition" varchar(50),
  "temperature" varchar(50),
  "current_location" varchar(225),
  "event_location" varchar(225),
  "user_id" integer
);

CREATE TABLE "forecast_day" (
  "forecast_id" integer PRIMARY KEY,
  "forecast_day" timestamp,
  "forecast_condition" varchar(50),
  "forecast_temperature" varchar(50),
  "forecast_location" varchar(225),
  "user_id" integer,
  "weather_id" integer
);

CREATE TABLE "activitiesLog" (
  "activitylog_id" integer PRIMARY KEY,
  "event" varchar(225),
  "event_time" timestamp,
  "user_id" integer,
  "task_id" integer
);

COMMENT ON COLUMN "categories"."task_id" IS 'foreign key to users table';

COMMENT ON COLUMN "tasks"."description" IS 'Content of the task';

COMMENT ON COLUMN "tasks"."category_id" IS 'foreign key to Categories table';

COMMENT ON COLUMN "tasks"."user_id" IS 'foreign key to users table';

COMMENT ON COLUMN "notifications"."user_id" IS 'foreign key to users table';

COMMENT ON COLUMN "notifications"."task_id" IS 'foreign key to tasks table';

COMMENT ON COLUMN "reports"."user_id" IS 'foreign key to users table';

COMMENT ON COLUMN "weather"."user_id" IS 'foreign key to users table';

COMMENT ON COLUMN "forecast_day"."user_id" IS 'foreign key to users table';

COMMENT ON COLUMN "forecast_day"."weather_id" IS 'foreign key to weather table';

COMMENT ON COLUMN "activitiesLog"."user_id" IS 'foreign key to users table';

COMMENT ON COLUMN "activitiesLog"."task_id" IS 'foreign key to tasks table';

CREATE TABLE "tasks_categories" (
  "tasks_task_id" integer,
  "categories_category_id" integer,
  PRIMARY KEY ("tasks_task_id", "categories_category_id")
);

ALTER TABLE "tasks_categories" ADD FOREIGN KEY ("tasks_task_id") REFERENCES "tasks" ("task_id");

ALTER TABLE "tasks_categories" ADD FOREIGN KEY ("categories_category_id") REFERENCES "categories" ("category_id");


ALTER TABLE "tasks" ADD FOREIGN KEY ("task_id") REFERENCES "users" ("user_id");

ALTER TABLE "reports" ADD FOREIGN KEY ("report_id") REFERENCES "users" ("user_id");

ALTER TABLE "notifications" ADD FOREIGN KEY ("notification_id") REFERENCES "users" ("user_id");

ALTER TABLE "tasks" ADD FOREIGN KEY ("task_id") REFERENCES "weather" ("weather_id");

ALTER TABLE "forecast_day" ADD FOREIGN KEY ("forecast_id") REFERENCES "weather" ("weather_id");

ALTER TABLE "forecast_day" ADD FOREIGN KEY ("forecast_id") REFERENCES "users" ("user_id");

ALTER TABLE "activitiesLog" ADD FOREIGN KEY ("activitylog_id") REFERENCES "users" ("user_id");

ALTER TABLE "notifications" ADD FOREIGN KEY ("notification_id") REFERENCES "tasks" ("task_id");

ALTER TABLE "activitiesLog" ADD FOREIGN KEY ("activitylog_id") REFERENCES "tasks" ("task_id");
