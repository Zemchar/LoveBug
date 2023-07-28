FROM mcr.microsoft.com/dotnet/runtime:6.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["BugNest/BugNest.csproj", "BugNest/"]
RUN dotnet restore "BugNest/BugNest.csproj"
COPY . .
WORKDIR "/src/BugNest"
RUN dotnet build "BugNest.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "BugNest.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "BugNest.dll"]
EXPOSE 9128
EXPOSE 9129
