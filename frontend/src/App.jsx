import React, { useMemo, useState } from "react";
import {
  BadgeDollarSign,
  BookOpen,
  Briefcase,
  Bug,
  Calculator,
  ChevronRight,
  Coins,
  Factory,
  Gamepad2,
  HandCoins,
  HeartPulse,
  HelpCircle,
  Landmark,
  Minus,
  Plus,
  Scale,
  School,
  Table2,
  TrendingUp,
  User,
  Users,
  Vote,
  Wheat,
  X,
} from "lucide-react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

const roles = [
  {
    id: "working",
    label: "Clase Trabajadora",
    short: "Obrera",
    color: "red",
    icon: Users,
    accent: "border-red-400/60 bg-red-600/15 text-red-100",
  },
  {
    id: "capitalist",
    label: "Clase Capitalista",
    short: "Capitalista",
    color: "blue",
    icon: Factory,
    accent: "border-sky-400/60 bg-sky-600/15 text-sky-100",
  },
  {
    id: "middle",
    label: "Clase Media",
    short: "Media",
    color: "amber",
    icon: Briefcase,
    accent: "border-amber-300/60 bg-amber-400/15 text-amber-100",
  },
  {
    id: "state",
    label: "El Estado",
    short: "Estado",
    color: "zinc",
    icon: Landmark,
    accent: "border-zinc-300/50 bg-zinc-500/15 text-zinc-100",
  },
];

const fiscalPolicies = [
  {
    id: "A",
    title: "Sector publico amplio",
    subtitle: "Impuestos altos",
    taxRate: 0.32,
    ideology: "Socialismo",
  },
  {
    id: "B",
    title: "Pacto social",
    subtitle: "Impuestos medios",
    taxRate: 0.22,
    ideology: "Centro",
  },
  {
    id: "C",
    title: "Estado minimo",
    subtitle: "Impuestos bajos",
    taxRate: 0.12,
    ideology: "Neoliberalismo",
  },
];

const pricePolicies = [
  { id: "free", title: "Gratis", subtitle: "Servicio publico", price: 0.75 },
  { id: "mixed", title: "5V", subtitle: "Mercado mixto", price: 5 },
  { id: "private", title: "10V", subtitle: "Servicio privado", price: 10 },
];

const prosperityGoals = [
  { id: "basic", label: "Basica", value: 2.31 },
  { id: "dignified", label: "Digna", value: 2.97 },
  { id: "strong", label: "Fuerte", value: 3.63 },
  { id: "historic", label: "Historica", value: 4.29 },
];

const companyDeck = [
  {
    id: "farms",
    name: "Granjas cooperativas",
    industry: "Agricultura",
    slots: 4,
    output: "Comida",
    outputPerWorker: 2,
    icon: Wheat,
    accent: "from-emerald-500/25 to-emerald-950/20",
  },
  {
    id: "clinic",
    name: "Clinica del barrio",
    industry: "Salud",
    slots: 3,
    output: "Salud",
    outputPerWorker: 1,
    icon: HeartPulse,
    accent: "from-red-500/25 to-red-950/20",
  },
  {
    id: "college",
    name: "Colegio tecnico",
    industry: "Educacion",
    slots: 3,
    output: "Educacion",
    outputPerWorker: 1,
    icon: School,
    accent: "from-sky-500/25 to-sky-950/20",
  },
  {
    id: "factory",
    name: "Fabrica privada",
    industry: "Industria",
    slots: 5,
    output: "Salarios",
    outputPerWorker: 1,
    icon: Factory,
    accent: "from-zinc-400/20 to-zinc-950/10",
  },
  {
    id: "media",
    name: "Centro cultural",
    industry: "Ocio",
    slots: 2,
    output: "Ocio",
    outputPerWorker: 1,
    icon: Vote,
    accent: "from-violet-500/20 to-violet-950/20",
  },
];

const initialAssignments = {
  farms: 2,
  clinic: 1,
  college: 1,
  factory: 3,
  media: 1,
};

function numberFormat(value, digits = 2) {
  return new Intl.NumberFormat("es-CO", {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  }).format(Number.isFinite(value) ? value : 0);
}

function currentRoleById(roleId) {
  return roles.find((role) => role.id === roleId) ?? roles[0];
}

function WorkerPips({ total, active = total, color = "red", size = "h-5 w-5" }) {
  const visible = Math.min(total, 24);
  const colorClass = {
    red: "fill-red-500 text-red-300",
    blue: "fill-sky-500 text-sky-300",
    amber: "fill-amber-400 text-amber-200",
    zinc: "fill-zinc-500 text-zinc-300",
  }[color];

  return (
    <div className="flex flex-wrap gap-1.5" aria-label={`${total} trabajadores`}>
      {Array.from({ length: visible }).map((_, index) => (
        <User
          key={index}
          className={`${size} ${index < active ? colorClass : "text-zinc-700"}`}
          strokeWidth={2.4}
        />
      ))}
      {total > visible && (
        <span className="rounded-md border border-white/10 bg-zinc-900 px-2 py-0.5 text-xs font-black text-zinc-100">
          +{total - visible}
        </span>
      )}
    </div>
  );
}

function Stepper({ value, min = 0, max = 100, step = 1, suffix = "", onChange }) {
  return (
    <div className="flex items-center gap-1">
      <button
        className="grid h-8 w-8 place-items-center rounded-md border border-white/10 bg-zinc-950 text-zinc-200 disabled:opacity-30"
        onClick={() => onChange(Math.max(min, value - step))}
        disabled={value <= min}
        title="Reducir"
      >
        <Minus size={15} />
      </button>
      <span className="min-w-20 rounded-md border border-white/10 bg-black/20 px-2 py-1 text-center font-black text-zinc-50">
        {numberFormat(value, step < 1 ? 2 : 0)}
        {suffix}
      </span>
      <button
        className="grid h-8 w-8 place-items-center rounded-md border border-white/10 bg-zinc-950 text-zinc-200 disabled:opacity-30"
        onClick={() => onChange(Math.min(max, value + step))}
        disabled={value >= max}
        title="Aumentar"
      >
        <Plus size={15} />
      </button>
    </div>
  );
}

function Header({ activeRoleId, setActiveRoleId, round, nextTurn, openTutorial }) {
  const activeRole = currentRoleById(activeRoleId);
  const ActiveIcon = activeRole.icon;

  return (
    <header className="sticky top-0 z-20 border-b border-white/10 bg-zinc-950/95 backdrop-blur">
      <div className="mx-auto grid max-w-7xl gap-4 px-4 py-4">
        <div className="flex flex-col justify-between gap-3 lg:flex-row lg:items-center">
          <div className="flex items-center gap-3">
            <div className={`grid h-12 w-12 place-items-center rounded-md border ${activeRole.accent}`}>
              <ActiveIcon size={26} />
            </div>
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.22em] text-zinc-400">Hotseat multijugador</p>
              <h1 className="text-2xl font-black text-zinc-50">Hegemony: Lead Your Class to Victory</h1>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              className="flex h-10 items-center gap-2 rounded-md border border-white/10 bg-zinc-900 px-3 font-bold text-zinc-100 hover:border-red-300/60"
              onClick={openTutorial}
            >
              <HelpCircle size={17} />
              Como jugar
            </button>
            <div className="rounded-md border border-white/10 bg-zinc-900 px-3 py-2 text-sm text-zinc-300">
              Ronda <span className="font-black text-zinc-50">{round}</span> de <span className="font-black text-zinc-50">5</span>
            </div>
            <button
              className="flex h-10 items-center gap-2 rounded-md bg-red-600 px-4 font-black text-white hover:bg-red-500"
              onClick={nextTurn}
            >
              Siguiente Turno
              <ChevronRight size={18} />
            </button>
          </div>
        </div>

        <div className="grid gap-2 sm:grid-cols-4">
          {roles.map((role) => {
            const Icon = role.icon;
            const active = activeRoleId === role.id;

            return (
              <button
                key={role.id}
                className={`rounded-md border p-3 text-left transition ${
                  active ? role.accent : "border-white/10 bg-white/[0.03] text-zinc-400 hover:border-white/30"
                }`}
                onClick={() => setActiveRoleId(role.id)}
              >
                <div className="flex items-center gap-2">
                  <Icon size={18} />
                  <span className="font-black">{role.label}</span>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}

function PolicyButtons({ options, selectedId, onSelect, activeClass = "border-red-300 bg-red-500/20 text-red-50" }) {
  return (
    <div className="grid gap-2 sm:grid-cols-3">
      {options.map((option) => {
        const active = selectedId === option.id;

        return (
          <button
            key={option.id}
            className={`rounded-md border p-3 text-left transition ${
              active ? activeClass : "border-white/10 bg-white/[0.03] text-zinc-300 hover:border-white/30"
            }`}
            onClick={() => onSelect(option)}
          >
            <p className="font-black">{option.title}</p>
            <p className="text-sm opacity-80">{option.subtitle}</p>
            {"ideology" in option && <p className="mt-2 text-xs uppercase tracking-wide opacity-70">{option.ideology}</p>}
          </button>
        );
      })}
    </div>
  );
}

function EconomySnapshot({ economy, boardState, round, activeRoleId }) {
  const activeRole = currentRoleById(activeRoleId);
  const ActiveIcon = activeRole.icon;

  return (
    <section className="rounded-md border border-white/10 bg-zinc-900/70 p-4">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className={`grid h-10 w-10 place-items-center rounded-md border ${activeRole.accent}`}>
            <ActiveIcon size={21} />
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Turno activo</p>
            <h2 className="text-xl font-black text-zinc-50">{activeRole.label}</h2>
          </div>
        </div>
        <div className="rounded-md border border-white/10 bg-black/20 px-3 py-2 text-sm text-zinc-300">Ronda {round}/5</div>
      </div>

      <div className="grid gap-3 md:grid-cols-4">
        <div className="rounded-md border border-white/10 bg-black/20 p-3">
          <div className="flex items-center gap-2 text-zinc-400">
            <Scale size={17} />
            <span className="text-xs uppercase tracking-wide">Impuesto</span>
          </div>
          <p className="mt-2 text-2xl font-black text-zinc-50">{numberFormat(economy.taxRate * 100, 0)}%</p>
        </div>
        <div className="rounded-md border border-white/10 bg-black/20 p-3">
          <div className="flex items-center gap-2 text-zinc-400">
            <HeartPulse size={17} />
            <span className="text-xs uppercase tracking-wide">Salud</span>
          </div>
          <p className="mt-2 text-2xl font-black text-red-100">{numberFormat(economy.healthPrice, 2)}V</p>
        </div>
        <div className="rounded-md border border-white/10 bg-black/20 p-3">
          <div className="flex items-center gap-2 text-zinc-400">
            <School size={17} />
            <span className="text-xs uppercase tracking-wide">Educacion</span>
          </div>
          <p className="mt-2 text-2xl font-black text-sky-100">{numberFormat(economy.educationPrice, 2)}V</p>
        </div>
        <div className="rounded-md border border-white/10 bg-black/20 p-3">
          <div className="flex items-center gap-2 text-zinc-400">
            <Coins size={17} />
            <span className="text-xs uppercase tracking-wide">Ingreso ofrecido</span>
          </div>
          <p className="mt-2 text-2xl font-black text-emerald-100">{numberFormat(boardState.offeredIncome, 0)}V</p>
        </div>
      </div>
    </section>
  );
}

function StatePanel({ economy, setEconomy }) {
  return (
    <section className="rounded-md border border-zinc-300/30 bg-zinc-900/80 p-5">
      <div className="mb-4 flex items-center gap-3">
        <Landmark className="text-zinc-200" size={24} />
        <div>
          <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">El Estado</p>
          <h2 className="text-2xl font-black text-zinc-50">Ajustar politicas publicas</h2>
        </div>
      </div>

      <div className="grid gap-4">
        <div>
          <p className="mb-2 text-sm font-bold text-zinc-300">Politica fiscal</p>
          <PolicyButtons
            options={fiscalPolicies}
            selectedId={economy.fiscalPolicy.id}
            activeClass="border-zinc-200 bg-zinc-100/10 text-zinc-50"
            onSelect={(policy) =>
              setEconomy((current) => ({
                ...current,
                fiscalPolicy: policy,
                taxRate: policy.taxRate,
                log: [`El Estado movio Politica Fiscal a ${policy.id}: ${policy.subtitle}.`, ...current.log].slice(0, 6),
              }))
            }
          />
        </div>

        <div className="rounded-md border border-white/10 bg-black/20 p-4">
          <div className="mb-3 flex items-center justify-between gap-3">
            <div>
              <p className="font-black text-zinc-50">Legitimidad estatal</p>
              <p className="text-sm text-zinc-400">Representa la confianza de las clases.</p>
            </div>
            <Stepper
              value={economy.legitimacy}
              min={0}
              max={12}
              onChange={(value) => setEconomy((current) => ({ ...current, legitimacy: value }))}
            />
          </div>
          <p className="text-sm leading-6 text-zinc-400">
            En el juego original, el Estado intenta sostener legitimidad mientras administra impuestos y servicios.
          </p>
        </div>
      </div>
    </section>
  );
}

function MarketPanel({ roleId, economy, setEconomy }) {
  const isCapitalist = roleId === "capitalist";
  const role = currentRoleById(roleId);
  const Icon = role.icon;
  const panelClass = isCapitalist ? "border-sky-400/30 bg-sky-950/20" : "border-amber-300/30 bg-amber-950/20";
  const activeClass = isCapitalist ? "border-sky-300 bg-sky-400/15 text-sky-50" : "border-amber-300 bg-amber-400/15 text-amber-50";
  const wageKey = isCapitalist ? "capitalistWage" : "middleWage";

  return (
    <section className={`rounded-md border p-5 ${panelClass}`}>
      <div className="mb-4 flex items-center gap-3">
        <Icon size={24} />
        <div>
          <p className="text-xs uppercase tracking-[0.22em] text-zinc-400">{role.label}</p>
          <h2 className="text-2xl font-black text-zinc-50">Definir mercado y salarios</h2>
        </div>
      </div>

      <div className="grid gap-5">
        <div>
          <p className="mb-2 text-sm font-bold text-zinc-300">Precio de Salud</p>
          <PolicyButtons
            options={pricePolicies}
            selectedId={economy.healthPolicy.id}
            activeClass={activeClass}
            onSelect={(policy) =>
              setEconomy((current) => ({
                ...current,
                healthPolicy: policy,
                healthPrice: policy.price,
                log: [`${role.short} ajusto Salud a ${policy.title}.`, ...current.log].slice(0, 6),
              }))
            }
          />
        </div>

        <div>
          <p className="mb-2 text-sm font-bold text-zinc-300">Precio de Educacion</p>
          <PolicyButtons
            options={pricePolicies}
            selectedId={economy.educationPolicy.id}
            activeClass={activeClass}
            onSelect={(policy) =>
              setEconomy((current) => ({
                ...current,
                educationPolicy: policy,
                educationPrice: policy.price,
                log: [`${role.short} ajusto Educacion a ${policy.title}.`, ...current.log].slice(0, 6),
              }))
            }
          />
        </div>

        <div className="rounded-md border border-white/10 bg-black/20 p-4">
          <div className="mb-3 flex items-center justify-between gap-3">
            <div>
              <p className="font-black text-zinc-50">Salario ofrecido</p>
              <p className="text-sm text-zinc-400">Afecta el ingreso disponible de la Clase Trabajadora.</p>
            </div>
            <Stepper
              value={economy[wageKey]}
              min={10}
              max={120}
              step={5}
              suffix="V"
              onChange={(value) =>
                setEconomy((current) => ({
                  ...current,
                  [wageKey]: value,
                  log: [`${role.short} fijo salario en ${value}V.`, ...current.log].slice(0, 6),
                }))
              }
            />
          </div>
        </div>
      </div>
    </section>
  );
}

function CompanyCard({ company, assigned, availableWorkers, onChange }) {
  const Icon = company.icon;
  const canAdd = availableWorkers > 0 && assigned < company.slots;
  const canRemove = assigned > 0;

  return (
    <article className={`rounded-md border border-white/10 bg-gradient-to-br ${company.accent} p-4`}>
      <div className="mb-4 flex items-start justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-zinc-400">{company.industry}</p>
          <h3 className="mt-1 text-lg font-black text-zinc-50">{company.name}</h3>
        </div>
        <div className="grid h-10 w-10 place-items-center rounded-md border border-white/10 bg-zinc-950/70 text-red-100">
          <Icon size={22} />
        </div>
      </div>

      <div className="mb-4 rounded-md border border-white/10 bg-black/20 p-2">
        <WorkerPips total={company.slots} active={assigned} color="red" />
      </div>

      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-zinc-500">Produccion</p>
          <p className="font-bold text-zinc-200">
            {company.outputPerWorker} {company.output} / obrero
          </p>
        </div>
        <div className="flex items-center gap-1.5">
          <button
            className="grid h-9 w-9 place-items-center rounded-md border border-white/10 bg-zinc-950/70 text-zinc-200 disabled:cursor-not-allowed disabled:opacity-30"
            onClick={() => onChange(company.id, assigned - 1)}
            disabled={!canRemove}
            title="Retirar obrero"
          >
            <Minus size={16} />
          </button>
          <button
            className="grid h-9 w-9 place-items-center rounded-md border border-red-300/40 bg-red-600/25 text-red-50 disabled:cursor-not-allowed disabled:opacity-30"
            onClick={() => onChange(company.id, assigned + 1)}
            disabled={!canAdd}
            title="Asignar obrero"
          >
            <Plus size={16} />
          </button>
        </div>
      </div>
    </article>
  );
}

function WorkingPanel({
  population,
  setPopulation,
  goal,
  setGoal,
  assignments,
  updateAssignment,
  availableWorkers,
  boardState,
  economy,
  loading,
  error,
  calculateIncome,
}) {
  return (
    <section className="rounded-md border border-red-400/40 bg-red-950/20 p-5">
      <div className="mb-4 flex flex-col justify-between gap-3 lg:flex-row lg:items-start">
        <div className="flex items-center gap-3">
          <Users className="text-red-200" size={25} />
          <div>
            <p className="text-xs uppercase tracking-[0.22em] text-red-300">Clase Trabajadora</p>
            <h2 className="text-2xl font-black text-zinc-50">Asignar obreros y negociar bienestar</h2>
          </div>
        </div>
        <div className="rounded-md border border-red-400/30 bg-black/20 p-3">
          <div className="mb-2 flex items-center justify-between gap-3">
            <span className="text-sm font-bold text-zinc-300">Poblacion</span>
            <Stepper value={population} min={8} max={48} onChange={(value) => setPopulation(value)} />
          </div>
          <WorkerPips total={population} active={population} color="red" size="h-4 w-4" />
        </div>
      </div>

      <div className="mb-5 grid gap-3 lg:grid-cols-[1fr_280px]">
        <div className="rounded-md border border-white/10 bg-black/20 p-4">
          <p className="mb-3 text-sm font-bold text-zinc-300">Meta de prosperidad</p>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
            {prosperityGoals.map((option) => (
              <button
                key={option.id}
                className={`rounded-md border px-3 py-2 font-black ${
                  goal.id === option.id
                    ? "border-red-300 bg-red-500 text-white"
                    : "border-white/10 bg-white/[0.03] text-zinc-300 hover:border-red-400"
                }`}
                onClick={() => setGoal(option)}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-md border border-white/10 bg-black/20 p-4">
          <p className="text-xs uppercase tracking-wide text-zinc-500">Resumen obrero</p>
          <div className="mt-2 grid gap-2 text-sm text-zinc-300">
            <div className="flex justify-between">
              <span>Libres</span>
              <span className="font-black text-red-100">{availableWorkers}</span>
            </div>
            <div className="flex justify-between">
              <span>Comida faltante</span>
              <span className="font-black text-amber-100">{boardState.foodGap}</span>
            </div>
            <div className="flex justify-between">
              <span>Ingreso ofrecido</span>
              <span className="font-black text-emerald-100">{numberFormat(boardState.offeredIncome, 0)}V</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
        {companyDeck.map((company) => (
          <CompanyCard
            key={company.id}
            company={company}
            assigned={assignments[company.id]}
            availableWorkers={availableWorkers}
            onChange={updateAssignment}
          />
        ))}
      </div>

      <div className="mt-5 rounded-md border border-red-400/40 bg-zinc-950/70 p-4">
        <div className="mb-4 grid gap-2 text-sm text-zinc-300 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <p className="text-xs uppercase tracking-wide text-zinc-500">Impuesto vigente</p>
            <p className="font-black text-zinc-50">{numberFormat(economy.taxRate * 100, 0)}%</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-zinc-500">Precio salud</p>
            <p className="font-black text-red-100">{numberFormat(economy.healthPrice, 2)}V</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-zinc-500">Precio educacion</p>
            <p className="font-black text-sky-100">{numberFormat(economy.educationPrice, 2)}V</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-zinc-500">Ocio</p>
            <p className="font-black text-violet-100">{boardState.leisureInitial}</p>
          </div>
        </div>

        <button
          className="flex h-14 w-full items-center justify-center gap-3 rounded-md bg-red-600 px-4 text-base font-black text-white shadow-lg shadow-red-950/40 transition hover:bg-red-500 disabled:cursor-not-allowed disabled:opacity-60"
          onClick={calculateIncome}
          disabled={loading}
        >
          {loading ? <Calculator className="animate-pulse" size={22} /> : <BadgeDollarSign size={22} />}
          {loading ? "Calculando..." : "Calcular Ingreso Minimo Necesario"}
        </button>

        {error && (
          <p className="mt-3 rounded-md border border-red-400/40 bg-red-500/10 p-3 text-sm text-red-100">{error}</p>
        )}
      </div>
    </section>
  );
}

function TutorialModal({ open, onClose }) {
  if (!open) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-40 grid place-items-center bg-black/75 px-4 backdrop-blur-sm">
      <div className="w-full max-w-3xl rounded-md border border-white/10 bg-zinc-950 p-6 shadow-2xl shadow-black">
        <div className="mb-5 flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="grid h-12 w-12 place-items-center rounded-md border border-red-400/40 bg-red-600/20 text-red-100">
              <BookOpen size={25} />
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-red-300">Guia progresiva</p>
              <h2 className="text-2xl font-black text-zinc-50">Como jugar este prototipo</h2>
            </div>
          </div>
          <button
            className="grid h-9 w-9 place-items-center rounded-md border border-white/10 bg-zinc-900 text-zinc-300 hover:border-red-300"
            onClick={onClose}
            title="Cerrar"
          >
            <X size={18} />
          </button>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-md border border-zinc-300/20 bg-zinc-900 p-4">
            <Landmark className="mb-3 text-zinc-200" size={24} />
            <h3 className="font-black text-zinc-50">1. El Estado</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Cambia la politica fiscal. Mas impuestos reducen el ingreso libre de la Clase Trabajadora, pero simulan un Estado con mas capacidad de bienestar.
            </p>
          </div>
          <div className="rounded-md border border-sky-300/20 bg-sky-950/20 p-4">
            <Factory className="mb-3 text-sky-200" size={24} />
            <h3 className="font-black text-zinc-50">2. Mercado</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Capitalistas y Clase Media ajustan precios de salud, educacion y salarios. Esas decisiones cambian el costo de cubrir necesidades.
            </p>
          </div>
          <div className="rounded-md border border-red-300/20 bg-red-950/20 p-4">
            <Calculator className="mb-3 text-red-200" size={24} />
            <h3 className="font-black text-zinc-50">3. Clase Obrera</h3>
            <p className="mt-2 text-sm leading-6 text-zinc-400">
              Asigna obreros y calcula cuanto ingreso minimo debe exigir. El backend usa Newton-Raphson sin mostrar ecuaciones al jugador.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function ResultModal({ result, boardState, economy, onClose }) {
  if (!result) {
    return null;
  }

  const gap = Math.max(0, result.I_star - boardState.offeredIncome);
  const enoughIncome = gap <= 0.01;

  return (
    <div className="fixed inset-0 z-40 grid place-items-center bg-black/75 px-4 backdrop-blur-sm">
      <div className="w-full max-w-2xl rounded-md border border-red-400/50 bg-zinc-950 p-6 shadow-2xl shadow-red-950/40">
        <div className="mb-5 flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="grid h-12 w-12 place-items-center rounded-md bg-red-600 text-white">
              <HandCoins size={26} />
            </div>
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-red-300">Resolucion sindical</p>
              <h2 className="text-2xl font-black text-zinc-50">La mesa economica respondio</h2>
            </div>
          </div>
          <button
            className="grid h-9 w-9 place-items-center rounded-md border border-white/10 bg-zinc-900 text-zinc-300 hover:border-red-300"
            onClick={onClose}
            title="Cerrar"
          >
            <X size={18} />
          </button>
        </div>

        <p className="text-lg leading-8 text-zinc-100">
          Con los nuevos impuestos del Estado y los precios del mercado, la Clase Trabajadora necesita{" "}
          <span className="font-black text-red-200">{numberFormat(result.I_star, 2)}V</span> para sobrevivir y alcanzar su meta de prosperidad.
        </p>

        <p className={`mt-3 rounded-md border p-3 text-sm ${enoughIncome ? "border-emerald-300/30 bg-emerald-500/10 text-emerald-100" : "border-amber-300/30 bg-amber-500/10 text-amber-100"}`}>
          {enoughIncome
            ? `Los salarios ofrecidos cubren la meta. Sobran ${numberFormat(Math.abs(gap), 2)}V para sostener bienestar.`
            : `Con los salarios actuales faltan ${numberFormat(gap, 2)}V. La Clase Obrera puede exigir mejores salarios o politicas mas favorables.`}
        </p>

        <div className="mt-5 grid gap-3 sm:grid-cols-4">
          <div className="rounded-md border border-white/10 bg-white/[0.04] p-3">
            <p className="text-xs uppercase tracking-wide text-zinc-500">Impuesto</p>
            <p className="mt-1 text-xl font-black text-zinc-100">{numberFormat(economy.taxRate * 100, 0)}%</p>
          </div>
          <div className="rounded-md border border-white/10 bg-white/[0.04] p-3">
            <p className="text-xs uppercase tracking-wide text-zinc-500">Ingreso ofrecido</p>
            <p className="mt-1 text-xl font-black text-emerald-100">{numberFormat(boardState.offeredIncome, 0)}V</p>
          </div>
          <div className="rounded-md border border-white/10 bg-white/[0.04] p-3">
            <p className="text-xs uppercase tracking-wide text-zinc-500">Comida</p>
            <p className="mt-1 text-xl font-black text-amber-100">{numberFormat(result.mandatory_food_cost, 2)}V</p>
          </div>
          <div className="rounded-md border border-white/10 bg-white/[0.04] p-3">
            <p className="text-xs uppercase tracking-wide text-zinc-500">Newton</p>
            <p className="mt-1 text-xl font-black text-sky-100">{result.iterations} it.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function TeacherPanel({ open, onClose, result, payload, boardState, economy }) {
  const chartData = useMemo(
    () =>
      result?.history?.map((step) => ({
        iteration: step.iteration,
        estimate: Number(step.estimate.toFixed(4)),
        error: step.relative_error ?? 0,
      })) ?? [],
    [result],
  );

  return (
    <aside
      className={`fixed right-0 top-0 z-30 h-screen w-full max-w-xl transform overflow-y-auto border-l border-red-500/30 bg-zinc-950 p-5 shadow-2xl shadow-black transition-transform duration-300 ${
        open ? "translate-x-0" : "translate-x-full"
      }`}
    >
      <div className="mb-5 flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-red-300">Modo profesor</p>
          <h2 className="text-2xl font-black text-zinc-50">Analisis numerico oculto</h2>
        </div>
        <button
          className="grid h-9 w-9 place-items-center rounded-md border border-white/10 bg-zinc-900 text-zinc-300 hover:border-red-300"
          onClick={onClose}
          title="Ocultar panel"
        >
          <X size={18} />
        </button>
      </div>

      <div className="grid gap-4">
        <section className="rounded-md border border-white/10 bg-white/[0.03] p-4">
          <div className="mb-3 flex items-center gap-2 text-red-100">
            <Calculator size={18} />
            <h3 className="font-black">Metodo usado: Newton-Raphson</h3>
          </div>
          <div className="grid gap-2 text-sm text-zinc-300 sm:grid-cols-2">
            <p>Raiz calculada: {result ? `${numberFormat(result.I_star, 6)}V` : "Sin ejecutar"}</p>
            <p>Iteraciones: {result?.iterations ?? 0}</p>
            <p>Error final: {result ? result.final_error.toExponential(3) : "0.000e+0"}</p>
            <p>Meta continua: {numberFormat(payload["S*"], 2)}</p>
            <p>tau: {numberFormat(economy.taxRate, 2)}</p>
            <p>Ingreso ofrecido: {numberFormat(boardState.offeredIncome, 0)}V</p>
          </div>
        </section>

        <section className="rounded-md border border-white/10 bg-white/[0.03] p-4">
          <div className="mb-3 flex items-center gap-2 text-zinc-100">
            <TrendingUp size={18} />
            <h3 className="font-black">Convergencia</h3>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 10, right: 16, bottom: 6, left: 0 }}>
                <CartesianGrid stroke="#ffffff14" />
                <XAxis dataKey="iteration" stroke="#a1a1aa" />
                <YAxis stroke="#a1a1aa" width={76} />
                <Tooltip
                  contentStyle={{
                    background: "#09090b",
                    border: "1px solid rgba(255,255,255,0.14)",
                    borderRadius: "6px",
                    color: "#f4f4f5",
                  }}
                />
                <Line type="monotone" dataKey="estimate" stroke="#f87171" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="rounded-md border border-white/10 bg-white/[0.03] p-4">
          <div className="mb-3 flex items-center gap-2 text-zinc-100">
            <Table2 size={18} />
            <h3 className="font-black">Tabla de iteraciones</h3>
          </div>
          <div className="max-h-72 overflow-auto rounded-md border border-white/10">
            <table className="w-full min-w-[520px] text-left text-sm">
              <thead className="bg-zinc-900 text-xs uppercase tracking-wide text-zinc-400">
                <tr>
                  <th className="px-3 py-2">k</th>
                  <th className="px-3 py-2">Estimacion</th>
                  <th className="px-3 py-2">f(I)</th>
                  <th className="px-3 py-2">Error</th>
                </tr>
              </thead>
              <tbody>
                {(result?.history ?? []).map((step) => (
                  <tr key={step.iteration} className="border-t border-white/10 text-zinc-200">
                    <td className="px-3 py-2">{step.iteration}</td>
                    <td className="px-3 py-2">{numberFormat(step.estimate, 6)}</td>
                    <td className="px-3 py-2">{step.function_value.toExponential(3)}</td>
                    <td className="px-3 py-2">
                      {step.relative_error === null || step.relative_error === undefined
                        ? "-"
                        : step.relative_error.toExponential(3)}
                    </td>
                  </tr>
                ))}
                {!result && (
                  <tr>
                    <td className="px-3 py-4 text-zinc-500" colSpan={4}>
                      La Clase Trabajadora debe ejecutar el calculo para ver el historial.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </aside>
  );
}

function buildFinalScores({ result, boardState, economy, goal, population, round }) {
  const requiredIncome = result?.I_star ?? boardState.offeredIncome + 120;
  const workerGap = Math.max(0, requiredIncome - boardState.offeredIncome);
  const workerCoverage = Math.max(0, Math.min(1, boardState.offeredIncome / Math.max(requiredIncome, 1)));
  const publicServiceDiscount = Math.max(0, 10 - economy.healthPrice) + Math.max(0, 10 - economy.educationPrice);
  const capitalistMargin = Math.max(0, 120 - economy.capitalistWage) + economy.healthPrice * 2 + economy.educationPrice;
  const middleBalance = Math.max(0, 80 - Math.abs(economy.middleWage - 45)) + Math.max(0, 8 - economy.educationPrice) * 3;
  const stateBalance = economy.legitimacy * 7 + Math.max(0, 0.35 - Math.abs(economy.taxRate - 0.22)) * 120 + publicServiceDiscount * 2;

  const scores = [
    {
      role: roles[0],
      points: Math.round(workerCoverage * 70 + goal.value * 9 + boardState.healthInitial * 4 + boardState.educationInitial * 4 + boardState.leisureInitial * 3 - workerGap * 0.08),
      reason:
        workerGap <= 0.01
          ? "Cubrio comida, salud, educacion y ocio con los salarios negociados."
          : `Quedo por debajo del ingreso necesario por ${numberFormat(workerGap, 2)}V.`,
    },
    {
      role: roles[1],
      points: Math.round(capitalistMargin + Math.max(0, round - 1) * 4),
      reason: "Maximizo rentas manteniendo salarios y precios de mercado favorables a sus empresas.",
    },
    {
      role: roles[2],
      points: Math.round(middleBalance + boardState.educationInitial * 5 + boardState.healthInitial * 3),
      reason: "Sostuvo servicios, salarios intermedios y presencia productiva en salud y educacion.",
    },
    {
      role: roles[3],
      points: Math.round(stateBalance),
      reason: "Conservo legitimidad y equilibrio fiscal mientras las politicas afectaban a todas las clases.",
    },
  ].map((score) => ({ ...score, points: Math.max(0, score.points) }));

  return scores.sort((a, b) => b.points - a.points);
}

function FinalScreen({ scores, round, onRestart, onBackToBoard }) {
  const winner = scores[0];
  const WinnerIcon = winner.role.icon;

  return (
    <main className="min-h-screen bg-zinc-950 px-4 py-6 text-zinc-100">
      <div className="mx-auto grid max-w-6xl gap-5">
        <section className="rounded-md border border-red-400/40 bg-red-950/20 p-6 shadow-2xl shadow-black">
          <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-center">
            <div className="flex items-center gap-4">
              <div className={`grid h-16 w-16 place-items-center rounded-md border ${winner.role.accent}`}>
                <WinnerIcon size={34} />
              </div>
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.25em] text-red-300">Final de la ronda {round}</p>
                <h1 className="mt-1 text-3xl font-black text-zinc-50">Gana {winner.role.label}</h1>
                <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-300">{winner.reason}</p>
              </div>
            </div>
            <div className="rounded-md border border-white/10 bg-black/20 p-4 text-center">
              <p className="text-xs uppercase tracking-wide text-zinc-500">Puntos de Victoria</p>
              <p className="text-5xl font-black text-red-100">{winner.points}</p>
            </div>
          </div>
        </section>

        <section className="grid gap-3 md:grid-cols-2">
          {scores.map((score, index) => {
            const Icon = score.role.icon;

            return (
              <article key={score.role.id} className={`rounded-md border p-4 ${index === 0 ? score.role.accent : "border-white/10 bg-zinc-900/70"}`}>
                <div className="mb-3 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <Icon size={24} />
                    <div>
                      <p className="text-xs uppercase tracking-wide opacity-70">Posicion {index + 1}</p>
                      <h2 className="text-xl font-black">{score.role.label}</h2>
                    </div>
                  </div>
                  <p className="text-3xl font-black">{score.points}</p>
                </div>
                <p className="text-sm leading-6 opacity-80">{score.reason}</p>
              </article>
            );
          })}
        </section>

        <section className="rounded-md border border-white/10 bg-zinc-900/70 p-5">
          <h2 className="mb-3 text-xl font-black text-zinc-50">Lectura para la sustentacion</h2>
          <p className="text-sm leading-7 text-zinc-300">
            La pantalla final compara objetivos asimetricos: bienestar obrero, beneficio empresarial, estabilidad de clase media y legitimidad estatal.
            El dato clave de la Clase Trabajadora viene del backend: Newton-Raphson calcula el ingreso minimo necesario y el tablero lo interpreta como
            una consecuencia politica y economica, no como una ecuacion visible para el jugador.
          </p>
        </section>

        <div className="flex flex-wrap gap-3">
          <button className="rounded-md bg-red-600 px-5 py-3 font-black text-white hover:bg-red-500" onClick={onRestart}>
            Nueva partida
          </button>
          <button className="rounded-md border border-white/10 bg-zinc-900 px-5 py-3 font-black text-zinc-100 hover:border-red-300" onClick={onBackToBoard}>
            Volver al tablero
          </button>
        </div>
      </div>
    </main>
  );
}

export default function App() {
  const [activeRoleId, setActiveRoleId] = useState("working");
  const [round, setRound] = useState(1);
  const [population, setPopulation] = useState(10);
  const [goal, setGoal] = useState(prosperityGoals[1]);
  const [assignments, setAssignments] = useState(initialAssignments);
  const [economy, setEconomy] = useState({
    fiscalPolicy: fiscalPolicies[1],
    taxRate: fiscalPolicies[1].taxRate,
    healthPolicy: pricePolicies[1],
    healthPrice: pricePolicies[1].price,
    educationPolicy: pricePolicies[1],
    educationPrice: pricePolicies[1].price,
    capitalistWage: 55,
    middleWage: 38,
    legitimacy: 6,
    log: ["La ronda inicia con pacto social, servicios mixtos y salarios base."],
  });
  const [result, setResult] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [teacherOpen, setTeacherOpen] = useState(false);
  const [tutorialOpen, setTutorialOpen] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const assignedWorkers = useMemo(
    () => Object.values(assignments).reduce((total, value) => total + value, 0),
    [assignments],
  );
  const availableWorkers = Math.max(0, population - assignedWorkers);

  const boardState = useMemo(() => {
    const foodAvailable = 2 + assignments.farms * 2;
    const healthInitial = assignments.clinic;
    const educationInitial = assignments.college;
    const leisureInitial = assignments.media;
    const offeredIncome =
      assignments.factory * economy.capitalistWage +
      (assignments.clinic + assignments.college) * economy.middleWage +
      assignments.farms * 24 +
      assignments.media * 18;

    return {
      foodAvailable,
      healthInitial,
      educationInitial,
      leisureInitial,
      offeredIncome,
      foodGap: Math.max(0, population - foodAvailable),
    };
  }, [assignments, economy.capitalistWage, economy.middleWage, population]);

  const payload = useMemo(
    () => ({
      P: population,
      tau: economy.taxRate,
      F0: boardState.foodAvailable,
      p_f: 4,
      H0: boardState.healthInitial,
      E0: boardState.educationInitial,
      L0: boardState.leisureInitial,
      p_h: economy.healthPrice,
      p_e: economy.educationPrice,
      p_l: 10,
      "S*": goal.value,
      alpha_h: 0.4,
      alpha_e: 0.35,
      alpha_l: 0.25,
      rho_h: 0.4,
      rho_e: 0.35,
      rho_l: 0.25,
      offered_income: boardState.offeredIncome,
      initial_guess: Math.max(300, boardState.offeredIncome),
      tolerance: 1e-7,
      max_iterations: 100,
    }),
    [boardState, economy.educationPrice, economy.healthPrice, economy.taxRate, goal.value, population],
  );

  const finalScores = useMemo(
    () => buildFinalScores({ result, boardState, economy, goal, population, round }),
    [boardState, economy, goal, population, result, round],
  );

  function nextTurn() {
    const index = roles.findIndex((role) => role.id === activeRoleId);
    const nextIndex = (index + 1) % roles.length;

    if (nextIndex === 0) {
      if (round >= 5) {
        setGameOver(true);
        setEconomy((current) => ({
          ...current,
          log: ["La quinta ronda termino. Se calcula la puntuacion final.", ...current.log].slice(0, 6),
        }));
        return;
      }

      setRound((current) => current + 1);
    }

    setActiveRoleId(roles[nextIndex].id);
  }

  function restartGame() {
    setActiveRoleId("working");
    setRound(1);
    setPopulation(10);
    setGoal(prosperityGoals[1]);
    setAssignments(initialAssignments);
    setEconomy({
      fiscalPolicy: fiscalPolicies[1],
      taxRate: fiscalPolicies[1].taxRate,
      healthPolicy: pricePolicies[1],
      healthPrice: pricePolicies[1].price,
      educationPolicy: pricePolicies[1],
      educationPrice: pricePolicies[1].price,
      capitalistWage: 55,
      middleWage: 38,
      legitimacy: 6,
      log: ["La ronda inicia con pacto social, servicios mixtos y salarios base."],
    });
    setResult(null);
    setShowResult(false);
    setTeacherOpen(false);
    setTutorialOpen(false);
    setGameOver(false);
    setError("");
  }

  function updateAssignment(companyId, nextValue) {
    const company = companyDeck.find((item) => item.id === companyId);
    if (!company) {
      return;
    }

    const bounded = Math.max(0, Math.min(company.slots, nextValue));
    const nextAssignments = { ...assignments, [companyId]: bounded };
    const nextTotal = Object.values(nextAssignments).reduce((total, value) => total + value, 0);

    if (nextTotal <= population) {
      setAssignments(nextAssignments);
    }
  }

  async function calculateIncome() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/api/calculate-income`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const details = await response.json().catch(() => ({}));
        throw new Error(details.detail || "No se pudo calcular el ingreso minimo.");
      }

      const data = await response.json();
      setResult(data);
      setShowResult(true);
      setEconomy((current) => ({
        ...current,
        log: [`La Clase Trabajadora calculo un ingreso minimo de ${numberFormat(data.I_star, 2)}V.`, ...current.log].slice(0, 6),
      }));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  function renderActivePanel() {
    if (activeRoleId === "state") {
      return <StatePanel economy={economy} setEconomy={setEconomy} />;
    }

    if (activeRoleId === "capitalist" || activeRoleId === "middle") {
      return <MarketPanel roleId={activeRoleId} economy={economy} setEconomy={setEconomy} />;
    }

    return (
      <WorkingPanel
        population={population}
        setPopulation={(value) => setPopulation(Math.max(assignedWorkers, value))}
        goal={goal}
        setGoal={setGoal}
        assignments={assignments}
        updateAssignment={updateAssignment}
        availableWorkers={availableWorkers}
        boardState={boardState}
        economy={economy}
        loading={loading}
        error={error}
        calculateIncome={calculateIncome}
      />
    );
  }

  if (gameOver) {
    return (
      <FinalScreen
        scores={finalScores}
        round={round}
        onRestart={restartGame}
        onBackToBoard={() => setGameOver(false)}
      />
    );
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <Header
        activeRoleId={activeRoleId}
        setActiveRoleId={setActiveRoleId}
        round={round}
        nextTurn={nextTurn}
        openTutorial={() => setTutorialOpen(true)}
      />

      <button
        className="fixed bottom-5 right-5 z-20 flex items-center gap-2 rounded-md border border-red-400/40 bg-zinc-950 px-4 py-3 font-black text-red-100 shadow-2xl shadow-black hover:bg-red-950/40"
        onClick={() => setTeacherOpen(true)}
      >
        <Bug size={18} />
        Modo profesor
      </button>

      <div className="mx-auto grid max-w-7xl gap-5 px-4 py-5 xl:grid-cols-[1fr_360px]">
        <section className="grid content-start gap-5">
          <EconomySnapshot economy={economy} boardState={boardState} round={round} activeRoleId={activeRoleId} />
          {renderActivePanel()}
        </section>

        <aside className="grid content-start gap-5">
          <section className="rounded-md border border-white/10 bg-zinc-900/70 p-4">
            <div className="mb-4 flex items-center gap-3">
              <Gamepad2 className="text-red-200" size={22} />
              <div>
                <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Estado del tablero</p>
                <h2 className="text-xl font-black text-zinc-50">Economia nacional</h2>
              </div>
            </div>
            <div className="grid gap-3 text-sm text-zinc-300">
              <div className="flex justify-between border-b border-white/10 pb-2">
                <span>Politica Fiscal</span>
                <span className="font-black text-zinc-50">{economy.fiscalPolicy.id}</span>
              </div>
              <div className="flex justify-between border-b border-white/10 pb-2">
                <span>Salud</span>
                <span className="font-black text-red-100">{numberFormat(economy.healthPrice, 2)}V</span>
              </div>
              <div className="flex justify-between border-b border-white/10 pb-2">
                <span>Educacion</span>
                <span className="font-black text-sky-100">{numberFormat(economy.educationPrice, 2)}V</span>
              </div>
              <div className="flex justify-between border-b border-white/10 pb-2">
                <span>Trabajadores libres</span>
                <span className="font-black text-red-100">{availableWorkers}</span>
              </div>
              <div className="flex justify-between">
                <span>Meta obrera</span>
                <span className="font-black text-emerald-100">{goal.label}</span>
              </div>
            </div>
          </section>

          <section className="rounded-md border border-white/10 bg-zinc-900/70 p-4">
            <div className="mb-4 flex items-center gap-3">
              <BookOpen className="text-amber-100" size={20} />
              <h2 className="text-xl font-black text-zinc-50">Registro de ronda</h2>
            </div>
            <div className="grid gap-2">
              {economy.log.map((entry, index) => (
                <p key={`${entry}-${index}`} className="rounded-md border border-white/10 bg-black/20 p-3 text-sm leading-6 text-zinc-300">
                  {entry}
                </p>
              ))}
            </div>
          </section>
        </aside>
      </div>

      <TutorialModal open={tutorialOpen} onClose={() => setTutorialOpen(false)} />
      <ResultModal
        result={showResult ? result : null}
        boardState={boardState}
        economy={economy}
        onClose={() => setShowResult(false)}
      />
      <TeacherPanel
        open={teacherOpen}
        onClose={() => setTeacherOpen(false)}
        result={result}
        payload={payload}
        boardState={boardState}
        economy={economy}
      />
    </main>
  );
}
