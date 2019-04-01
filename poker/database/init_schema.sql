--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.6
-- Dumped by pg_dump version 9.6.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: deck; Type: TABLE; Schema: public; Owner: hyu
--

CREATE TABLE deck (
    id integer NOT NULL,
    round_id integer,
    cards text[] NOT NULL,
    current_card_position integer NOT NULL
);


ALTER TABLE deck OWNER TO hyu;

--
-- Name: deck_id_seq; Type: SEQUENCE; Schema: public; Owner: hyu
--

CREATE SEQUENCE deck_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE deck_id_seq OWNER TO hyu;

--
-- Name: deck_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hyu
--

ALTER SEQUENCE deck_id_seq OWNED BY deck.id;


--
-- Name: game_end_score; Type: TABLE; Schema: public; Owner: hyu
--

CREATE TABLE game_end_score (
    id integer NOT NULL,
    round_id integer,
    users_and_hands jsonb[],
    winnings jsonb[]
);


ALTER TABLE game_end_score OWNER TO hyu;

--
-- Name: game_end_score_id_seq; Type: SEQUENCE; Schema: public; Owner: hyu
--

CREATE SEQUENCE game_end_score_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE game_end_score_id_seq OWNER TO hyu;

--
-- Name: game_end_score_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hyu
--

ALTER SEQUENCE game_end_score_id_seq OWNED BY game_end_score.id;


--
-- Name: lobby; Type: TABLE; Schema: public; Owner: hyu
--

CREATE TABLE lobby (
    id integer NOT NULL,
    state integer NOT NULL,
    code text
);


ALTER TABLE lobby OWNER TO hyu;

--
-- Name: lobby_id_seq; Type: SEQUENCE; Schema: public; Owner: hyu
--

CREATE SEQUENCE lobby_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE lobby_id_seq OWNER TO hyu;

--
-- Name: lobby_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hyu
--

ALTER SEQUENCE lobby_id_seq OWNED BY lobby.id;


--
-- Name: player_status; Type: TABLE; Schema: public; Owner: hyu
--

CREATE TABLE player_status (
    id integer NOT NULL,
    money integer NOT NULL,
    in_round boolean NOT NULL,
    bet integer,
    last_action integer,
    is_current_player boolean NOT NULL,
    player_turn integer,
    hand text[],
    blind text
);


ALTER TABLE player_status OWNER TO hyu;

--
-- Name: player_status_id_seq; Type: SEQUENCE; Schema: public; Owner: hyu
--

CREATE SEQUENCE player_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE player_status_id_seq OWNER TO hyu;

--
-- Name: player_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hyu
--

ALTER SEQUENCE player_status_id_seq OWNED BY player_status.id;


--
-- Name: round; Type: TABLE; Schema: public; Owner: hyu
--

CREATE TABLE round (
    id integer NOT NULL,
    lobby_id integer,
    state integer NOT NULL,
    pot integer NOT NULL,
    board text[]
);


ALTER TABLE round OWNER TO hyu;

--
-- Name: round_id_seq; Type: SEQUENCE; Schema: public; Owner: hyu
--

CREATE SEQUENCE round_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE round_id_seq OWNER TO hyu;

--
-- Name: round_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hyu
--

ALTER SEQUENCE round_id_seq OWNED BY round.id;


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: hyu
--

CREATE TABLE sessions (
    id integer NOT NULL,
    session_id character varying(255),
    data bytea,
    expiry timestamp without time zone
);


ALTER TABLE sessions OWNER TO hyu;

--
-- Name: sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: hyu
--

CREATE SEQUENCE sessions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sessions_id_seq OWNER TO hyu;

--
-- Name: sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hyu
--

ALTER SEQUENCE sessions_id_seq OWNED BY sessions.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: hyu
--

CREATE TABLE users (
    id integer NOT NULL,
    username text,
    password text,
    display_name text,
    is_anonymous boolean,
    lobby_id integer,
    player_status_id integer,
    round_id integer
);


ALTER TABLE users OWNER TO hyu;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: hyu
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO hyu;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hyu
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: deck id; Type: DEFAULT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY deck ALTER COLUMN id SET DEFAULT nextval('deck_id_seq'::regclass);


--
-- Name: game_end_score id; Type: DEFAULT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY game_end_score ALTER COLUMN id SET DEFAULT nextval('game_end_score_id_seq'::regclass);


--
-- Name: lobby id; Type: DEFAULT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY lobby ALTER COLUMN id SET DEFAULT nextval('lobby_id_seq'::regclass);


--
-- Name: player_status id; Type: DEFAULT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY player_status ALTER COLUMN id SET DEFAULT nextval('player_status_id_seq'::regclass);


--
-- Name: round id; Type: DEFAULT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY round ALTER COLUMN id SET DEFAULT nextval('round_id_seq'::regclass);


--
-- Name: sessions id; Type: DEFAULT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY sessions ALTER COLUMN id SET DEFAULT nextval('sessions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: deck deck_pkey; Type: CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY deck
    ADD CONSTRAINT deck_pkey PRIMARY KEY (id);


--
-- Name: game_end_score game_end_score_pkey; Type: CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY game_end_score
    ADD CONSTRAINT game_end_score_pkey PRIMARY KEY (id);


--
-- Name: lobby lobby_pkey; Type: CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY lobby
    ADD CONSTRAINT lobby_pkey PRIMARY KEY (id);


--
-- Name: player_status player_status_pkey; Type: CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY player_status
    ADD CONSTRAINT player_status_pkey PRIMARY KEY (id);


--
-- Name: round round_pkey; Type: CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY round
    ADD CONSTRAINT round_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_session_id_key; Type: CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY sessions
    ADD CONSTRAINT sessions_session_id_key UNIQUE (session_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_lobby_code; Type: INDEX; Schema: public; Owner: hyu
--

CREATE INDEX ix_lobby_code ON lobby USING btree (code);


--
-- Name: deck deck_round_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY deck
    ADD CONSTRAINT deck_round_id_fkey FOREIGN KEY (round_id) REFERENCES round(id);


--
-- Name: game_end_score game_end_score_round_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY game_end_score
    ADD CONSTRAINT game_end_score_round_id_fkey FOREIGN KEY (round_id) REFERENCES round(id);


--
-- Name: round round_lobby_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY round
    ADD CONSTRAINT round_lobby_id_fkey FOREIGN KEY (lobby_id) REFERENCES lobby(id);


--
-- Name: users users_lobby_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_lobby_id_fkey FOREIGN KEY (lobby_id) REFERENCES lobby(id);


--
-- Name: users users_player_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_player_status_id_fkey FOREIGN KEY (player_status_id) REFERENCES player_status(id);


--
-- Name: users users_round_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hyu
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_round_id_fkey FOREIGN KEY (round_id) REFERENCES round(id);


--
-- PostgreSQL database dump complete
--

