# Client (Flutter — web now, desktop later)

## Setup

Requires the Flutter SDK: https://docs.flutter.dev/get-started/install

```bash
flutter pub get
```

## Run (web, pointing at your local backend)

```bash
flutter run -d chrome --dart-define=API_BASE_URL=http://localhost:8000
```

## Build for web (deployable demo)

```bash
flutter build web --dart-define=API_BASE_URL=https://your-deployed-backend
```

Output lands in `build/web/` — host it anywhere static (S3 + CloudFront,
Netlify, Vercel, etc.) to satisfy the "functional demo app URL" requirement.

## Desktop later

Once the web version works, enable a desktop target with zero code changes:

```bash
flutter config --enable-windows-desktop   # or macos-desktop / linux-desktop
flutter create --platforms=windows,macos,linux .
flutter run -d windows   # or macos / linux
```

## Structure

- `lib/models/` — plain data classes matching the FastAPI response shapes
- `lib/services/api_service.dart` — all HTTP + SSE calls live here (single choke point)
- `lib/screens/` — top-level screens
- `lib/widgets/` — reusable UI pieces
