--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: data; Type: DATABASE; Schema: -; Owner: postgres
--

ALTER DATABASE data OWNER TO postgres;

\connect data

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: annotation_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.annotation_types (
    id uuid NOT NULL,
    objective_name text NOT NULL,
    label_name text NOT NULL,
    value_type text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.annotation_types OWNER TO postgres;

--
-- Name: annotators; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.annotators (
    id uuid NOT NULL,
    name character varying NOT NULL,
    organization_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    age integer,
    gender character varying
);


ALTER TABLE public.annotators OWNER TO postgres;

--
-- Name: audio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audio (
    md5 text NOT NULL,
    file_name text NOT NULL,
    audio_format_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    custom_property json,
    duration integer NOT NULL,
    organization_id uuid NOT NULL
);


ALTER TABLE public.audio OWNER TO postgres;

--
-- Name: audio_annotations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audio_annotations (
    id uuid NOT NULL,
    annotation_type_id uuid NOT NULL,
    annotator_id uuid NOT NULL,
    dataset_id uuid,
    value text,
    start_time time without time zone NOT NULL,
    stop_time time without time zone NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    md5 text NOT NULL,
    version integer NOT NULL
);


ALTER TABLE public.audio_annotations OWNER TO postgres;

--
-- Name: audio_format; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audio_format (
    id uuid NOT NULL,
    bit_rate integer NOT NULL,
    sample_rate integer NOT NULL,
    channels integer NOT NULL
);


ALTER TABLE public.audio_format OWNER TO postgres;

--
-- Name: datasets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.datasets (
    id uuid NOT NULL,
    name text NOT NULL,
    type text NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    description text NOT NULL
);


ALTER TABLE public.datasets OWNER TO postgres;

--
-- Name: organizations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organizations (
    id uuid NOT NULL,
    name text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.organizations OWNER TO postgres;

--
-- Data for Name: annotation_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.annotation_types (id, objective_name, label_name, value_type, created_at) FROM stdin;
\.


--
-- Data for Name: annotators; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.annotators (id, name, organization_id, created_at, age, gender) FROM stdin;
\.


--
-- Data for Name: audio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audio (md5, file_name, audio_format_id, created_at, custom_property, duration, organization_id) FROM stdin;
\.


--
-- Data for Name: audio_annotations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audio_annotations (id, annotation_type_id, annotator_id, dataset_id, value, start_time, stop_time, created_at, md5, version) FROM stdin;
\.


--
-- Data for Name: audio_format; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audio_format (id, bit_rate, sample_rate, channels) FROM stdin;
\.


--
-- Data for Name: datasets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.datasets (id, name, type, created_at, description) FROM stdin;
\.


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organizations (id, name, created_at) FROM stdin;
\.


--
-- Name: annotation_types annotation_types_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotation_types
    ADD CONSTRAINT annotation_types_pk PRIMARY KEY (id);


--
-- Name: annotators annotators_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotators
    ADD CONSTRAINT annotators_pk PRIMARY KEY (id);


--
-- Name: audio_annotations audio_annotations_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audio_annotations
    ADD CONSTRAINT audio_annotations_pk PRIMARY KEY (id);


--
-- Name: audio_format audio_format_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audio_format
    ADD CONSTRAINT audio_format_pk PRIMARY KEY (id);


--
-- Name: audio data_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audio
    ADD CONSTRAINT data_pk PRIMARY KEY (md5);


--
-- Name: datasets datasets_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasets
    ADD CONSTRAINT datasets_pk PRIMARY KEY (id);


--
-- Name: organizations organizations_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pk PRIMARY KEY (id);


--
-- Name: annotation_types_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX annotation_types_id_uindex ON public.annotation_types USING btree (id);


--
-- Name: annotators_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX annotators_id_uindex ON public.annotators USING btree (id);


--
-- Name: audio_annotations_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX audio_annotations_id_uindex ON public.audio_annotations USING btree (id);


--
-- Name: audio_format_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX audio_format_id_uindex ON public.audio_format USING btree (id);


--
-- Name: data_md5_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX data_md5_uindex ON public.audio USING btree (md5);


--
-- Name: datasets_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX datasets_id_uindex ON public.datasets USING btree (id);


--
-- Name: datasets_name_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX datasets_name_uindex ON public.datasets USING btree (name);


--
-- Name: organizations_id_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX organizations_id_uindex ON public.organizations USING btree (id);


--
-- Name: organizations_name_uindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX organizations_name_uindex ON public.organizations USING btree (name);


--
-- Name: annotators annotators_organizations_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotators
    ADD CONSTRAINT annotators_organizations_id_fk FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: audio_annotations audio_annotations_annotation_types_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audio_annotations
    ADD CONSTRAINT audio_annotations_annotation_types_id_fk FOREIGN KEY (annotation_type_id) REFERENCES public.annotation_types(id);


--
-- Name: audio_annotations audio_annotations_annotators_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audio_annotations
    ADD CONSTRAINT audio_annotations_annotators_id_fk FOREIGN KEY (annotator_id) REFERENCES public.annotators(id);


--
-- Name: audio_annotations audio_annotations_data_md5_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audio_annotations
    ADD CONSTRAINT audio_annotations_data_md5_fk FOREIGN KEY (md5) REFERENCES public.audio(md5);


--
-- Name: audio_annotations audio_annotations_datasets_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audio_annotations
    ADD CONSTRAINT audio_annotations_datasets_id_fk FOREIGN KEY (dataset_id) REFERENCES public.datasets(id);


--
-- PostgreSQL database dump complete
--

