#!/bin/sh
env_file=".env"
if [ "$ENVIRONMENT" != "" ]; then
    env_file=".env.$ENVIRONMENT"
fi

db=`cat $env_file | sed -nE 's/^DATABASE_PATH *= *(.+)$/\1/p' | tr -d '"'`
schema_dir=`cat $env_file | sed -nE 's/^DATABASE_SCHEMA_DIR *= *(.+)$/\1/p' | tr -d '"'`
data_dir=`cat $env_file | sed -nE 's/^DATABASE_IMPORT_DATA_DIR *= *(.+)$/\1/p' | tr -d '"'`
delimeter=`cat $env_file | sed -nE 's/^DATABASE_IMPORT_DATA_DELIMETER *= *(.+)$/\1/p' | tr -d '"'`

while :; do
    case $1 in
        -h|-\?|--help)
            echo "Usage: create_db.sh [options]"
            echo "Options:"
            echo "  -h, --help                Show this help message and exit"
            echo "  -a, --db PATH             Specify the database path"
            echo "  -s, --schema DIR          Specify the schema directory"
            echo "  -f, --data DIR            Specify the data directory"
            echo "  -d, --delimeter DELIM     Specify the data delimiter (default is '|')"
            exit
            ;;
        -a|--db)
            if [ "$2" ]; then
                db=$2
                shift
            fi
            ;;
        -s|--schema)
            if [ "$2" ]; then
                schema_dir=$2
                shift
            fi
            ;;
        -f|--data)
            if [ "$2" ]; then
                data_dir=$2
                shift
            fi
            ;;
        -d|--delimeter)
            if [ "$2" ]; then
                delimeter=$2
                shift
            fi
            ;;
        --)
            shift
            break
            ;;
        -?*)
            printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
            ;;
        *)
            break
            ;;
    esac
    shift
done

if [ -z $db ]; then
    echo "Database path must be specified"
    exit 1
fi
if [ ! -d $schema_dir ]; then
    echo "Schema directory not found: $schema_dir"
    exit 1
fi
if [ ! -d $data_dir ]; then
    echo "Data directory not found: $data_dir"
    exit 1
fi
if [ -z $delimeter ]; then
    delimeter="|"
fi
schema=""
for f in `ls $schema_dir*.sql`; do
    schema="$schema $f"
done
data=""
for f in `ls $data_dir*.csv`; do
    data="$data $f"
done
printf "Creating database '$db' with:\nSchema:   $schema\nData:     $data\nDelimeter: $delimeter\n\n..."
`python -m app.db.creator $db -s$schema -f$data -d $delimeter`
printf "\rDone\n"