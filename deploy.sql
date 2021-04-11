drop table if exists flashcards;

create table flashcards (
	id serial primary key,
	question text,
	answer text
);

insert into
	flashcards (question, answer)
values
	('Good morning', 'お早うございます'),
	('Nice to meet you', '始めまして'),
	('Good evening', 'こんにちはす'),
	('Good night', 'おやすみなさい'),
	('Welcome', 'いらっしゃいませ')