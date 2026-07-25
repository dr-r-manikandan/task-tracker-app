import React, { useState, useMemo, useRef } from "react";
import {
  Plus, Trash2, Check, Search, X, Flag, Tag as TagIcon,
  Calendar, ChevronDown, ListChecks, CircleDot, Sparkles
} from "lucide-react";

const PRIORITIES = {
  critical: { label: "Critical", dot: "bg-red-500", text: "text-red-600", bg: "bg-red-50", border: "border-red-200" },
  high:     { label: "High",     dot: "bg-orange-500", text: "text-orange-600", bg: "bg-orange-50", border: "border-orange-200" },
  medium:   { label: "Medium",   dot: "bg-amber-500", text: "text-amber-600", bg: "bg-amber-50", border: "border-amber-200" },
  low:      { label: "Low",      dot: "bg-sky-500", text: "text-sky-600", bg: "bg-sky-50", border: "border-sky-200" },
};

const PRIORITY_ORDER = ["critical", "high", "medium", "low"];

const SEED_TASKS = [
  { id: 1, title: "Wire up GitHub Integration auth flow", priority: "critical", category: "backend", dueDate: "2026-07-25", completed: false },
  { id: 2, title: "Write positive tests for terraform-plan operation", priority: "high", category: "testing", dueDate: "2026-07-27", completed: false },
  { id: 3, title: "Draft rollback workflow example payloads", priority: "medium", category: "docs", dueDate: "", completed: false },
  { id: 4, title: "Review output.schema.json for deployment skill", priority: "high", category: "review", dueDate: "2026-07-26", completed: true },
  { id: 5, title: "Set up mock GitHub API responses", priority: "low", category: "testing", dueDate: "", completed: true },
];

function ticketId(n) {
  return `TASK-${String(n).padStart(3, "0")}`;
}

function formatDate(d) {
  if (!d) return null;
  const date = new Date(d + "T00:00:00");
  if (Number.isNaN(date.getTime())) return null;
  return date.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

function isOverdue(d, completed) {
  if (!d || completed) return false;
  const date = new Date(d + "T00:00:00");
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return date < today;
}

export default function TaskTracker() {
  const [tasks, setTasks] = useState(SEED_TASKS);
  const nextId = useRef(SEED_TASKS.length + 1);

  const [statusFilter, setStatusFilter] = useState("active"); // all | active | completed
  const [priorityFilter, setPriorityFilter] = useState("all");
  const [query, setQuery] = useState("");
  const [sortBy, setSortBy] = useState("priority"); // priority | due | created

  const [formOpen, setFormOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState("medium");
  const [category, setCategory] = useState("");
  const [dueDate, setDueDate] = useState("");
  const titleInputRef = useRef(null);

  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState("");

  const stats = useMemo(() => {
    const total = tasks.length;
    const completed = tasks.filter((t) => t.completed).length;
    const active = total - completed;
    const rate = total === 0 ? 0 : Math.round((completed / total) * 100);
    return { total, completed, active, rate };
  }, [tasks]);

  const visibleTasks = useMemo(() => {
    let list = [...tasks];

    if (statusFilter === "active") list = list.filter((t) => !t.completed);
    if (statusFilter === "completed") list = list.filter((t) => t.completed);

    if (priorityFilter !== "all") list = list.filter((t) => t.priority === priorityFilter);

    if (query.trim()) {
      const q = query.trim().toLowerCase();
      list = list.filter(
        (t) =>
          t.title.toLowerCase().includes(q) ||
          t.category.toLowerCase().includes(q) ||
          ticketId(t.id).toLowerCase().includes(q)
      );
    }

    list.sort((a, b) => {
      if (sortBy === "priority") {
        return PRIORITY_ORDER.indexOf(a.priority) - PRIORITY_ORDER.indexOf(b.priority);
      }
      if (sortBy === "due") {
        if (!a.dueDate && !b.dueDate) return 0;
        if (!a.dueDate) return 1;
        if (!b.dueDate) return -1;
        return a.dueDate.localeCompare(b.dueDate);
      }
      return b.id - a.id; // created, newest first
    });

    return list;
  }, [tasks, statusFilter, priorityFilter, query, sortBy]);

  function resetForm() {
    setTitle("");
    setPriority("medium");
    setCategory("");
    setDueDate("");
    setFormOpen(false);
  }

  function addTask(e) {
    e.preventDefault();
    const trimmed = title.trim();
    if (!trimmed) {
      titleInputRef.current?.focus();
      return;
    }
    const newTask = {
      id: nextId.current++,
      title: trimmed,
      priority,
      category: category.trim() || "general",
      dueDate,
      completed: false,
    };
    setTasks((prev) => [newTask, ...prev]);
    resetForm();
  }

  function toggleTask(id) {
    setTasks((prev) => prev.map((t) => (t.id === id ? { ...t, completed: !t.completed } : t)));
  }

  function deleteTask(id) {
    setTasks((prev) => prev.filter((t) => t.id !== id));
  }

  function startEdit(task) {
    setEditingId(task.id);
    setEditTitle(task.title);
  }

  function commitEdit(id) {
    const trimmed = editTitle.trim();
    setTasks((prev) => prev.map((t) => (t.id === id ? { ...t, title: trimmed || t.title } : t)));
    setEditingId(null);
  }

  return (
    <div className="min-h-screen w-full bg-slate-50 text-slate-900 font-sans">
      <div className="max-w-5xl mx-auto px-6 py-10">
        {/* Header */}
        <header className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center shadow-sm">
              <ListChecks className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-semibold tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                Taskboard
              </h1>
              <p className="text-sm text-slate-500">Frontend-only test harness · nothing here is saved</p>
            </div>
          </div>
          <button
            onClick={() => {
              setFormOpen((v) => !v);
              setTimeout(() => titleInputRef.current?.focus(), 0);
            }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700 active:scale-[0.98] transition"
          >
            <Plus className="w-4 h-4" />
            New task
          </button>
        </header>

        {/* Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
          <StatCard label="Total" value={stats.total} />
          <StatCard label="Active" value={stats.active} />
          <StatCard label="Completed" value={stats.completed} />
          <div className="rounded-xl bg-white border border-slate-200 p-4">
            <p className="text-xs font-medium text-slate-500 mb-2">Completion</p>
            <div className="flex items-center gap-2">
              <div className="flex-1 h-2 rounded-full bg-slate-100 overflow-hidden">
                <div
                  className="h-full bg-emerald-500 rounded-full transition-all"
                  style={{ width: `${stats.rate}%` }}
                />
              </div>
              <span className="text-sm font-semibold tabular-nums">{stats.rate}%</span>
            </div>
          </div>
        </div>

        {/* Add task form */}
        {formOpen && (
          <form
            onSubmit={addTask}
            className="mb-6 rounded-xl bg-white border border-slate-200 p-4 shadow-sm"
          >
            <div className="flex items-start gap-3">
              <input
                ref={titleInputRef}
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="What needs to get done?"
                className="flex-1 px-3 py-2 rounded-lg border border-slate-200 text-sm outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
              <button
                type="button"
                onClick={resetForm}
                className="p-2 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-50"
                aria-label="Cancel"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="flex flex-wrap gap-3 mt-3">
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="px-3 py-2 rounded-lg border border-slate-200 text-sm outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
              >
                {PRIORITY_ORDER.map((p) => (
                  <option key={p} value={p}>{PRIORITIES[p].label} priority</option>
                ))}
              </select>
              <input
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                placeholder="Category (optional)"
                className="px-3 py-2 rounded-lg border border-slate-200 text-sm outline-none focus:ring-2 focus:ring-indigo-500 w-40"
              />
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="px-3 py-2 rounded-lg border border-slate-200 text-sm outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <button
                type="submit"
                className="ml-auto px-4 py-2 rounded-lg bg-slate-900 text-white text-sm font-medium hover:bg-slate-800 active:scale-[0.98] transition"
              >
                Add task
              </button>
            </div>
          </form>
        )}

        {/* Toolbar */}
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <div className="flex rounded-lg border border-slate-200 bg-white p-1">
            {["active", "all", "completed"].map((s) => (
              <button
                key={s}
                onClick={() => setStatusFilter(s)}
                className={`px-3 py-1.5 rounded-md text-sm font-medium capitalize transition ${
                  statusFilter === s ? "bg-slate-900 text-white" : "text-slate-500 hover:text-slate-800"
                }`}
              >
                {s}
              </button>
            ))}
          </div>

          <div className="relative">
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              className="appearance-none pl-3 pr-8 py-2 rounded-lg border border-slate-200 bg-white text-sm outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="all">All priorities</option>
              {PRIORITY_ORDER.map((p) => (
                <option key={p} value={p}>{PRIORITIES[p].label}</option>
              ))}
            </select>
            <ChevronDown className="w-4 h-4 absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
          </div>

          <div className="relative">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="appearance-none pl-3 pr-8 py-2 rounded-lg border border-slate-200 bg-white text-sm outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="priority">Sort: priority</option>
              <option value="due">Sort: due date</option>
              <option value="created">Sort: newest</option>
            </select>
            <ChevronDown className="w-4 h-4 absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
          </div>

          <div className="relative flex-1 min-w-[180px]">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search tasks..."
              className="w-full pl-9 pr-3 py-2 rounded-lg border border-slate-200 bg-white text-sm outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        {/* Task list */}
        <div className="space-y-2">
          {visibleTasks.length === 0 && (
            <div className="text-center py-16 rounded-xl border border-dashed border-slate-300 bg-white">
              <Sparkles className="w-6 h-6 mx-auto text-slate-300 mb-2" />
              <p className="text-sm font-medium text-slate-600">No tasks match these filters</p>
              <p className="text-sm text-slate-400 mt-1">Try clearing a filter or add a new task.</p>
            </div>
          )}

          {visibleTasks.map((task) => {
            const p = PRIORITIES[task.priority];
            const overdue = isOverdue(task.dueDate, task.completed);
            return (
              <div
                key={task.id}
                className={`group flex items-center gap-3 rounded-xl bg-white border p-3.5 transition ${
                  task.completed ? "border-slate-100" : "border-slate-200 hover:border-slate-300"
                }`}
              >
                <button
                  onClick={() => toggleTask(task.id)}
                  aria-label={task.completed ? "Mark as active" : "Mark as complete"}
                  className={`w-5 h-5 shrink-0 rounded-full border-2 flex items-center justify-center transition ${
                    task.completed
                      ? "bg-emerald-500 border-emerald-500"
                      : "border-slate-300 hover:border-indigo-500"
                  }`}
                >
                  {task.completed && <Check className="w-3 h-3 text-white" strokeWidth={3} />}
                </button>

                <span
                  className="text-xs font-mono text-slate-400 shrink-0 w-[74px]"
                  style={{ fontFamily: "'Space Grotesk', monospace" }}
                >
                  {ticketId(task.id)}
                </span>

                <div className="flex-1 min-w-0">
                  {editingId === task.id ? (
                    <input
                      autoFocus
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      onBlur={() => commitEdit(task.id)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") commitEdit(task.id);
                        if (e.key === "Escape") setEditingId(null);
                      }}
                      className="w-full px-2 py-1 rounded-md border border-indigo-300 text-sm outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  ) : (
                    <button
                      onClick={() => startEdit(task)}
                      className={`text-sm text-left truncate block w-full ${
                        task.completed ? "line-through text-slate-400" : "text-slate-800"
                      }`}
                      title="Click to edit"
                    >
                      {task.title}
                    </button>
                  )}
                </div>

                <span className={`hidden sm:inline-flex items-center gap-1.5 text-xs font-medium px-2 py-1 rounded-full border shrink-0 ${p.bg} ${p.text} ${p.border}`}>
                  <Flag className="w-3 h-3" />
                  {p.label}
                </span>

                <span className="hidden md:inline-flex items-center gap-1.5 text-xs text-slate-500 shrink-0">
                  <TagIcon className="w-3 h-3" />
                  {task.category}
                </span>

                {task.dueDate && (
                  <span className={`hidden lg:inline-flex items-center gap-1.5 text-xs shrink-0 ${overdue ? "text-red-500 font-medium" : "text-slate-500"}`}>
                    <Calendar className="w-3 h-3" />
                    {formatDate(task.dueDate)}
                  </span>
                )}

                <button
                  onClick={() => deleteTask(task.id)}
                  aria-label="Delete task"
                  className="p-1.5 rounded-md text-slate-300 hover:text-red-500 hover:bg-red-50 opacity-0 group-hover:opacity-100 transition shrink-0"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            );
          })}
        </div>

        <footer className="mt-8 flex items-center gap-2 text-xs text-slate-400">
          <CircleDot className="w-3.5 h-3.5" />
          In-memory only — data resets on refresh. No backend, no database.
        </footer>
      </div>
    </div>
  );
}
function StatCard({ label, value }) {
  return (
    <div className="rounded-xl bg-white border border-slate-200 p-4">
      <p className="text-xs font-medium text-slate-500 mb-2">
        {label}
      </p>
      <p className="text-2xl font-bold text-slate-900">
        {value}
      </p>
    </div>
  );
}
