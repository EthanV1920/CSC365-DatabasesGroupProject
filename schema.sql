CREATE table
  traits (
    trait_id int generated always as identity not null PRIMARY KEY,
    agility int not null,
    damage int not null,
    control int not null
  );

CREATE table
  characters (
    character_id int generated always as identity not null PRIMARY KEY,
    name text not null,
    traits_id int REFERENCES traits (trait_id)
  );

create table
  public.users (
    user_id integer generated always as identity,
    timestamp timestamp with time zone null default now(),
    username text not null,
    level integer not null,
    constraint users_pkey primary key (user_id)
  ) tablespace pg_default;

create table
  public.carts (
    cart_id integer generated always as identity,
    timestamp timestamp with time zone null default now(),
    user_id integer null,
    checkout boolean not null default false,
    constraint carts_pkey primary key (cart_id),
    constraint carts_user_id_fkey foreign key (user_id) references users (user_id)
  ) tablespace pg_default;

create table
  public.cart_items (
    line_item_id integer generated always as identity,
    cart_id integer not null default 0,
    user_id integer null,
    character_id integer not null,
    constraint cart_items_pkey primary key (line_item_id),
    constraint cart_items_cart_id_fkey foreign key (cart_id) references carts (cart_id),
    constraint cart_items_user_id_fkey foreign key (user_id) references users (user_id),
    constraint cart_items_character_fkey foreign key (character_id) references characters (character_id)
  ) tablespace pg_default;

create table
  public.gold_ledger (
    ledger_id bigint generated by default as identity,
    user_id integer not null,
    created_at timestamp with time zone not null default now(),
    gold integer not null,
    constraint gold_ledger_user_id_fkey foreign key (user_id) references users (user_id),
    constraint gold_ledger_pkey primary key (ledger_id)
  ) tablespace pg_default;

create table
  public.characters_ledger (
    ledger_id bigint generated by default as identity,
    user_id integer not null,
    character_id integer not null,
    created_at timestamp with time zone not null default now(),
    constraint characters_ledger_user_id_fkey foreign key (user_id) references users (user_id),
    constraint characters_ledger_character_id_fkey foreign key (character_id) references characters (character_id),
    constraint characters_ledger_pkey primary key (ledger_id)
  ) tablespace pg_default;
