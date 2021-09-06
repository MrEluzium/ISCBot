create table users(
    id integer primary key not null,
    username text,
    school_id integer not null references schools(id),
    role text not null,
    user_id integer not null
);

create table schools(
    id integer primary key not null,
    school_name text not null,
    class_name text not null,
    editor_token text not null
);

create table homework(
    id integer primary key not null,
    subject text not null,
    title text not null,
    created_at TIMESTAMP DATE DEFAULT (date('now')),
    user_id integer not null,
    school_id integer not null references schools(id)
);

create table timetable(
    id integer primary key not null,
    day text not null,
    subject text not null,
    time text,
    school_id integer not null references schools(id)
);