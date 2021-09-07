/*
ISCBot. Telegram school helper for students.
Copyright (C) 2021 Artem Vorochaev (vorochaev2004@live.ru, github.com/Hymiside)
                   Artem Voronov (mreluzium@mail.ru, github.com/MrEluzium)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

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