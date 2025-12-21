--
-- PostgreSQL database dump
--

\restrict iLr7WnPypvfiyhc2zNivCiUmReKqpaMjmLyOtPHVyEqzQReqQLjy3iiM1O0kaRw

-- Dumped from database version 18.1 (Debian 18.1-1.pgdg13+2)
-- Dumped by pg_dump version 18.0

-- Started on 2025-12-21 11:30:15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 219 (class 1259 OID 24576)
-- Name: tasks; Type: TABLE; Schema: public; Owner: tasklist
--

CREATE TABLE public.tasks (
    description character varying(500) NOT NULL,
    active boolean CONSTRAINT tasks_status_not_null NOT NULL,
    id bigint NOT NULL,
    user_id integer,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone
);


ALTER TABLE public.tasks OWNER TO tasklist;

--
-- TOC entry 220 (class 1259 OID 24586)
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: tasklist
--

CREATE SEQUENCE public.tasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO tasklist;

--
-- TOC entry 3454 (class 0 OID 0)
-- Dependencies: 220
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tasklist
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- TOC entry 222 (class 1259 OID 24597)
-- Name: users; Type: TABLE; Schema: public; Owner: tasklist
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    password character varying(255) NOT NULL
);


ALTER TABLE public.users OWNER TO tasklist;

--
-- TOC entry 221 (class 1259 OID 24596)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: tasklist
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO tasklist;

--
-- TOC entry 3455 (class 0 OID 0)
-- Dependencies: 221
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tasklist
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 3294 (class 2604 OID 24587)
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: tasklist
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- TOC entry 3296 (class 2604 OID 24600)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: tasklist
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3298 (class 2606 OID 24595)
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: tasklist
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 3300 (class 2606 OID 24605)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: tasklist
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3301 (class 2606 OID 24606)
-- Name: tasks fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: tasklist
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id) NOT VALID;


-- Completed on 2025-12-21 11:30:16

--
-- PostgreSQL database dump complete
--

\unrestrict iLr7WnPypvfiyhc2zNivCiUmReKqpaMjmLyOtPHVyEqzQReqQLjy3iiM1O0kaRw

