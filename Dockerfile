# Stage 1: Build the application
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["BugNest/BugNest.csproj", "BugNest/"]
RUN dotnet restore "BugNest/BugNest.csproj"
COPY . .
WORKDIR "/src/BugNest"
RUN dotnet build "BugNest.csproj" -c Release -o /app/build
RUN dotnet publish "BugNest.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Stage 2: Create the runtime image
FROM mcr.microsoft.com/dotnet/runtime:6.0 AS final
WORKDIR /app

# Copy the published files from the build stage
COPY --from=build /app/publish .

# Copy the appsettings.json file into the container
COPY BugNest/appsettings.json .

# Expose the desired ports (if needed)
EXPOSE 9128
EXPOSE 9129

# Add the wait-for-it.sh script to the container
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Set the entrypoint script to wait for the database before running the .NET application
ENTRYPOINT ["/app/wait-for-it.sh", "my_mysql_db:3306", "-t", "20", "--", "dotnet", "BugNest.dll"]
