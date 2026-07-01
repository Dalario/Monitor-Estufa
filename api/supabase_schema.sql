-- Execute este SQL no Supabase:
-- Dashboard -> SQL Editor -> New query -> cole e clique em "Run".

create table if not exists leituras (
    id          bigint generated always as identity primary key,
    temperatura real        not null,
    umidade     real        not null,
    luz         real        not null,
    criado_em   timestamptz not null default now()
);

-- Índice para acelerar as consultas do histórico ordenadas por data.
create index if not exists idx_leituras_criado_em
    on leituras (criado_em desc);

-- Segurança: a API usa a chave service_role, que ignora o RLS.
-- Mantemos o RLS ligado e SEM políticas públicas para que a chave anon
-- (pública) não consiga ler nem escrever direto no banco.
alter table leituras enable row level security;
