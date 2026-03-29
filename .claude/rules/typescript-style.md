# TypeScript TSDoc and Type Annotations

## TSDoc Comments

All exported functions, classes, interfaces, and type aliases MUST have TSDoc comments (`/** ... */`). Internal helpers
may omit TSDoc only if the name and signature are fully self-explanatory.

### Required tags

- **Summary**: A single sentence describing what the symbol does, placed before any tags.
- **`@param`**: Every parameter with a brief description. Omit only for zero-parameter functions.
- **`@returns`**: What the return value represents. Omit only for `void` functions with no meaningful side effect
  description needed.
- **`@throws`**: Every error the function explicitly throws. Omit only if the function throws nothing.

### Optional tags

- **`@example`**: Include when usage is non-obvious or the function has complex input/output shapes.
- **`@remarks`**: Include for important caveats (e.g., mutates input, not idempotent).

### Example

```typescript
/**
 * Fetch changes from a monitored source since the given timestamp.
 *
 * @param sourceUrl - The URL of the source to check for changes.
 * @param since - Only return changes after this date.
 * @param options - Optional configuration for the request.
 * @param options.timeout - HTTP request timeout in milliseconds. Defaults to 30000.
 * @returns A list of Change objects ordered by timestamp ascending, or an empty array if none found.
 * @throws {SourceUnreachableError} If the source cannot be contacted within the timeout.
 * @throws {InvalidSourceError} If the URL does not point to a supported source type.
 */
export async function fetchChanges(
    sourceUrl: string,
    since: Date,
    options?: { timeout?: number },
): Promise<Change[]> { }
```

## Type Annotations

All TypeScript code MUST use explicit types. Specifically:

- **Function signatures**: Annotate every parameter and the return type. No exceptions for exported functions.
- **Exported interfaces and types**: Define explicit shapes; do not export bare object literals.
- **Avoid `any`**: Use `unknown` when the type is genuinely indeterminate. If `any` is truly unavoidable, add a
  `// eslint-disable-next-line` comment explaining why.
- **Prefer narrower types**: Use string literal unions, discriminated unions, and branded types over plain `string` or
  `number` when the domain warrants it.
- **Inferred return types**: Allowed for non-exported functions when the return type is obvious from the implementation.
  Exported functions must always have an explicit return type.
