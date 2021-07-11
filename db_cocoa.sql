-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 11 Jul 2021 pada 15.46
-- Versi server: 10.4.20-MariaDB
-- Versi PHP: 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_cocoa`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_device`
--

CREATE TABLE `tb_device` (
  `id` varchar(100) NOT NULL,
  `nama_device` varchar(45) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_fermentasi`
--

CREATE TABLE `tb_fermentasi` (
  `id_kotak` varchar(100) NOT NULL,
  `id_karung` varchar(100) NOT NULL,
  `suhu` decimal(10,0) NOT NULL,
  `ph` decimal(10,0) NOT NULL,
  `kelembapan` decimal(10,0) NOT NULL,
  `add_by` varchar(45) NOT NULL,
  `update_by` varchar(45) NOT NULL,
  `dt_add` date NOT NULL,
  `dt_update` date NOT NULL,
  `device` varchar(100) NOT NULL,
  `kondisi` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_kondisi`
--

CREATE TABLE `tb_kondisi` (
  `id` int(11) NOT NULL,
  `kondisi` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_order`
--

CREATE TABLE `tb_order` (
  `id_order` varchar(255) NOT NULL,
  `id_karung` varchar(100) NOT NULL,
  `berat` decimal(10,0) NOT NULL,
  `add_by` varchar(45) NOT NULL,
  `update_by` varchar(45) NOT NULL,
  `order_by` varchar(45) NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_otoritas`
--

CREATE TABLE `tb_otoritas` (
  `id` int(11) NOT NULL,
  `otoritas` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_panen`
--

CREATE TABLE `tb_panen` (
  `id_karung` varchar(100) NOT NULL,
  `berat_kotor` decimal(10,0) NOT NULL,
  `berat_bersih` decimal(10,0) NOT NULL,
  `add_by` varchar(45) NOT NULL,
  `update_by` varchar(45) NOT NULL,
  `dt_add` date NOT NULL,
  `dt_update` date NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_status`
--

CREATE TABLE `tb_status` (
  `id` int(11) NOT NULL,
  `status` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_status_alat`
--

CREATE TABLE `tb_status_alat` (
  `id` int(11) NOT NULL,
  `status` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `tb_user`
--

CREATE TABLE `tb_user` (
  `user_id` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `no_hp` varchar(100) NOT NULL,
  `password` varchar(256) NOT NULL,
  `dt_update` date NOT NULL,
  `dt_add` date NOT NULL,
  `dt_expired` date NOT NULL,
  `status` int(11) NOT NULL,
  `token` varchar(256) NOT NULL,
  `otoritas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `tb_device`
--
ALTER TABLE `tb_device`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `tb_fermentasi`
--
ALTER TABLE `tb_fermentasi`
  ADD PRIMARY KEY (`id_kotak`);

--
-- Indeks untuk tabel `tb_kondisi`
--
ALTER TABLE `tb_kondisi`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `tb_order`
--
ALTER TABLE `tb_order`
  ADD PRIMARY KEY (`id_order`);

--
-- Indeks untuk tabel `tb_otoritas`
--
ALTER TABLE `tb_otoritas`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `tb_panen`
--
ALTER TABLE `tb_panen`
  ADD PRIMARY KEY (`id_karung`);

--
-- Indeks untuk tabel `tb_status`
--
ALTER TABLE `tb_status`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `tb_status_alat`
--
ALTER TABLE `tb_status_alat`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `tb_user`
--
ALTER TABLE `tb_user`
  ADD PRIMARY KEY (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
